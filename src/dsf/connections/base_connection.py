import json
import select
import socket
import time
from typing import Optional, Protocol, TypeVar

from .exceptions import IncompatibleVersionException, InternalServerException, TaskCanceledException
from .init_messages import client_init_messages, server_init_message
from ..commands import responses


T_co = TypeVar("T_co", covariant=True)


class _FromJson(Protocol[T_co]):
    @classmethod
    def from_json(cls, data: dict[str, object]) -> T_co:
        ...


class BaseConnection:
    """
    Base class for connections that access the control server via the Duet API
    using a UNIX socket
    """

    def __init__(self, debug: bool = False, timeout: int = 3):
        self.debug = debug
        self.timeout = timeout
        self.socket: Optional[socket.socket] = None
        self.id: object | None = None
        self.input = ""

    def connect(self, socket_file: str) -> None:
        """Establish a connection to the given UNIX socket file."""
        raise NotImplementedError("BaseConnection.connect must be implemented by subclasses")

    def _connect(self, init_message: client_init_messages.ClientInitMessage, socket_file: str) -> None:
        """Establishes a connection to the given UNIX socket file"""

        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect(socket_file)
        self.socket.settimeout(self.timeout if self.timeout > 0 else None)
        # self.socket.setblocking(True)
        server_init_msg = server_init_message.ServerInitMessage.from_json(
            json.loads(self.socket.recv(50).decode("utf8"))
        )
        if not server_init_msg.is_compatible():
            raise IncompatibleVersionException(
                f"Incompatible API version (need {server_init_msg.PROTOCOL_VERSION}, got {server_init_msg.version})"
            )
        self.id = server_init_msg.id
        self.send(init_message)

        response = self.receive_response()
        if isinstance(response, responses.ErrorResponse):
            raise Exception(
                f"Could not set connection type {init_message.mode} ({response.error_type}: {response.error_message})"
            )

    def close(self) -> None:
        """Closes the current connection and disposes it"""
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def perform_command(self, command: object, cls: type[_FromJson[T_co]] | None = None) -> responses.Response:
        """Perform an arbitrary command"""
        self.send(command)

        response = self.receive_response()
        if isinstance(response, responses.Response):
            if cls is not None and response.result is not None:
                response.result = cls.from_json(response.result)
            return response

        if response.error_type == "TaskCanceledException":
            raise TaskCanceledException(response.error_message)

        raise InternalServerException(
            command, response.error_type, response.error_message
        )

    def send(self, msg: object) -> None:
        """Serialize an arbitrary object into JSON and send it to the server plus NL"""
        if self.socket is None:
            raise RuntimeError("socket is closed or missing")

        json_string = json.dumps(msg, separators=(",", ":"), default=lambda o: o.__dict__)
        if self.debug:
            print(f"send: {json_string}")
        self.socket.sendall(json_string.encode("utf8"))

    def receive(self, cls: type[_FromJson[T_co]]) -> T_co:
        """Receive a deserialized object from the server"""
        json_string = self.receive_json()
        return cls.from_json(json.loads(json_string))

    def receive_response(self) -> responses.Response | responses.ErrorResponse:
        """Receive a base response from the server"""
        json_string = self.receive_json()
        return responses.decode_response(json.loads(json_string))

    def has_data_available(self) -> bool:
        """Return whether buffered or socket data is available to be read without blocking."""
        if self.get_json_object_end_index(self.input) > 1:
            return True

        if not self.socket:
            return False

        readable, _, _ = select.select([self.socket], [], [], 0)
        if not readable:
            return False

        try:
            return bool(self.socket.recv(1, socket.MSG_PEEK | socket.MSG_DONTWAIT))
        except BlockingIOError:
            return False

    def receive_json(self) -> str:
        """Receive the JSON response from the server"""
        if not self.socket:
            raise RuntimeError("socket is closed or missing")

        json_string = self.input

        # There might be a full object waiting in the buffer
        end_index = self.get_json_object_end_index(json_string)
        if end_index > 1:
            # Save whatever is left in the buffer
            self.input = json_string[end_index:]
            # Limit to the first full JSON object
            json_string = json_string[:end_index]
        else:
            found = False
            start_time = time.time()
            while not found:
                if (self.timeout > 0) and (time.time() - start_time > self.timeout):
                    raise TimeoutError("Timeout while waiting for JSON response")

                # Refill the buffer and check again
                BUFF_SIZE = 4096  # 4 KiB
                data = b""
                part = b""
                while True:
                    try:
                        part = self.socket.recv(BUFF_SIZE)
                        data += part
                    except socket.timeout:
                        pass
                    except Exception as e:
                        raise e
                    # either 0 or end of data
                    if len(part) < BUFF_SIZE:
                        break

                json_string += data.decode("utf8")

                end_index = self.get_json_object_end_index(json_string)
                if end_index > 1:
                    # Save whatever is left in the buffer
                    self.input = json_string[end_index:]
                    # Limit to the first full JSON object
                    json_string = json_string[:end_index]
                    found = True

        if self.debug:
            print("recv:", json_string)
        return json_string

    @staticmethod
    def get_json_object_end_index(json_string: str) -> int:
        """Return the end index of the next full JSON object in the string"""
        count = 0
        index = 0
        while index < len(json_string):
            token = json_string[index]
            if token == "{":  # Found opening curly brace
                count += 1
            elif token == "}":  # Found closing curly brace
                count -= 1

            if count < 0:  # Unbalanced curly braces - incomplete input?
                return -1
            if count == 0:  # Found a complete object
                return index + 1

            index += 1

        return -1  # Nothing here
