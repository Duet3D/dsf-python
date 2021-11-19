"""
connections provides different classes for connections

    Python interface to DuetSoftwareFramework
    Copyright (C) 2020 Duet3D

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import json
import os
import socket
from typing import Optional

from . import DEFAULT_BACKLOG, SOCKET_FILE
from .commands import responses, basecommands, code, result, codechannel
from .commands.basecommands import MessageType, LogLevel
from .initmessages import serverinitmessage, clientinitmessages
from .http import HttpEndpointUnixSocket
from .models import MachineModel, ParsedFileInfo


class TaskCanceledException(Exception):
    """Exception returned by the server if the task has been cancelled remotely"""


class InternalServerException(Exception):
    """Exception returned by the server for an arbitrary problem"""

    def __init__(self, command, error_type: str, error_message: str):
        super().__init__("Internal Server Exception")
        self.command = command
        self.error_type = error_type
        self.error_message = error_message


class BaseConnection:
    """
    Base class for connections that access the control server via the Duet API
    using a UNIX socket
    """

    def __init__(self, debug: bool = False, timeout: int = 3):
        self.debug = debug
        self.timeout = timeout
        self.socket: Optional[socket.socket] = None
        self.id = None
        self.input = ""

    def connect(
        self, init_message: clientinitmessages.ClientInitMessage, socket_file: str
    ):
        """Establishes a connection to the given UNIX socket file"""

        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect(socket_file)
        self.socket.setblocking(True)
        server_init_message = serverinitmessage.ServerInitMessage.from_json(
            json.loads(self.socket.recv(50).decode("utf8"))
        )
        if not server_init_message.is_compatible():
            raise serverinitmessage.IncompatibleVersionException(
                "Incompatible API version (need {0}, got {1})".format(
                    server_init_message.PROTOCOL_VERSION, server_init_message.version
                )
            )
        self.id = server_init_message.id
        self.send(init_message)

        response = self.receive_response()
        if not response.success:
            raise Exception(
                "Could not set connection type {0} ({1}: {2})".format(
                    init_message.mode, response.error_type, response.error_message
                )
            )

    def close(self):
        """Closes the current connection and disposes it"""
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def perform_command(self, command, cls=None):
        """Perform an arbitrary command"""
        self.send(command)

        response = self.receive_response()
        if response.success:
            if cls is not None and response.result is not None:
                response.result = cls.from_json(response.result)
            return response

        if response.error_type == "TaskCanceledException":
            raise TaskCanceledException(response.error_message)

        raise InternalServerException(
            command, response.error_type, response.error_message
        )

    def send(self, msg):
        """Serialize an arbitrary object into JSON and send it to the server plus NL"""
        json_string = json.dumps(
            msg, separators=(",", ":"), default=lambda o: o.__dict__
        )
        if self.debug:
            print("send: {0}".format(json_string))
        self.socket.sendall(json_string.encode("utf8"))

    def receive(self, cls):
        """Receive a deserialized object from the server"""
        json_string = self.receive_json()
        return cls.from_json(json.loads(json_string))

    def receive_response(self):
        """Receive a base response from the server"""
        json_string = self.receive_json()
        return json.loads(json_string, object_hook=responses.decode_response)

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
            while not found:
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
                    if len(part) == 0:
                        raise TimeoutError
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
    def get_json_object_end_index(json_string: str):
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


class BaseCommandConnection(BaseConnection):
    """Base connection class for sending commands to the control server"""

    def flush(self, channel: codechannel.CodeChannel = codechannel.CodeChannel.SBC):
        """Wait for all pending codes of the given channel to finish"""
        return self.perform_command(basecommands.flush(channel))

    def add_http_endpoint(
        self,
        endpoint_type: basecommands.HttpEndpointType,
        namespace: str,
        path: str,
        is_upload_request: bool = False,
        backlog: int = DEFAULT_BACKLOG,
    ):
        """Add a new third-party HTTP endpoint in the format /machine/{ns}/{path}"""
        res = self.perform_command(
            basecommands.add_http_endpoint(
                endpoint_type, namespace, path, is_upload_request
            )
        )
        socket_file = res.result
        return HttpEndpointUnixSocket(
            endpoint_type, namespace, path, socket_file, backlog, self.debug
        )

    def add_user_session(
        self,
        access: basecommands.AccessLevel,
        tpe: basecommands.SessionType,
        origin: str,
        origin_port: int = None,
    ):
        """Add a new user session"""
        if origin_port is None:
            origin_port = os.getpid()

        res = self.perform_command(
            basecommands.add_user_session(access, tpe, origin, origin_port)
        )
        return int(res.result)

    def check_password(self, password: str):
        """Check the given password (see M551)"""
        return self.perform_command(basecommands.check_password(password))

    def get_file_info(self, file_name: str):
        """Parse a G-code file and returns file information about it"""
        res = self.perform_command(
            basecommands.get_file_info(file_name), ParsedFileInfo
        )
        return res.result

    def get_machine_model(self):
        """
        Retrieve the full object model of the machine.

        Deprecated: use get_object_model instead.
        """
        return self.get_object_model()

    def get_object_model(self):
        """Retrieve the full object model of the machine."""
        res = self.perform_command(basecommands.get_object_model(), MachineModel)
        return res.result

    def get_serialized_machine_model(self):
        """
        Optimized method to directly query the machine model UTF-8 JSON.

        Deprecated: use get_serialized_object_model instead.
        """
        return self.get_serialized_object_model()

    def get_serialized_object_model(self):
        """Optimized method to directly query the machine model UTF-8 JSON"""
        self.send(basecommands.get_object_model())
        return self.receive_json()

    def install_plugin(self, plugin_file: str):
        """Install or upgrade a plugin"""
        res = self.perform_command(basecommands.install_plugin(plugin_file))
        return res.result

    def lock_machine_model(self):
        """
        Lock the machine model for read/write access.
        It is MANDATORY to call unlock_object_model when write access has finished

        Deprecated: use lock_object_model instead
        """
        return self.lock_object_model()

    def lock_object_model(self):
        """
        Lock the machine model for read/write access.
        It is MANDATORY to call unlock_object_model when write access has finished
        """
        return self.perform_command(basecommands.lock_object_model())

    def patch_object_model(self, key: str, patch):
        """
        Apply a full patch to the object model. Use with care!
        """
        res = self.perform_command(basecommands.patch_object_model(key, patch))
        return res.result

    def perform_code(self, cde: code.Code):
        """Execute an arbitrary pre-parsed code"""
        res = self.perform_command(cde, result.CodeResult)
        return res.result

    def perform_simple_code(
        self,
        cde: str,
        channel: codechannel.CodeChannel = codechannel.CodeChannel.DEFAULT_CHANNEL,
    ):
        """Execute an arbitrary G/M/T-code in text form and return the result as a string"""
        res = self.perform_command(basecommands.simple_code(cde, channel))
        return res.result

    def remove_http_endpoint(
        self, endpoint_type: basecommands.HttpEndpointType, namespace: str, path: str
    ):
        """Remove an existing HTTP endpoint"""
        res = self.perform_command(
            basecommands.remove_http_endpoint(endpoint_type, namespace, path)
        )
        return res.result

    def remove_user_session(self, session_id: int):
        """Remove an existing HTTP endpoint"""
        res = self.perform_command(basecommands.remove_user_session(session_id))
        return res.result

    def resolve_path(self, path: str):
        """Resolve a RepRapFirmware-style file path to a real file path"""
        return self.perform_command(basecommands.resolve_path(path))

    def set_machine_model(self, path: str, value: str):
        """
        Set a given property to a certain value.
        Make sure to lock the object model before calling this

        Deprecated: use set_object_model instead
        """
        return self.set_object_model(path, value)

    def set_object_model(self, path: str, value: str):
        """
        Set a given property to a certain value.
        Make sure to lock the object model before calling this
        """
        return self.perform_command(basecommands.set_object_model(path, value))

    def set_plugin_data(self, plugin: str, key: str, value: str):
        """Set custom plugin data in the object model"""
        res = self.perform_command(basecommands.set_plugin_data(plugin, key, value))
        return res.result

    def set_update_status(self, is_updating: bool):
        """Override the current machin staeus if a software update is in progress"""
        res = self.perform_command(basecommands.set_update_status(is_updating))
        return res.result

    def start_plugin(self, plugin: str):
        """Start a plugin"""
        res = self.perform_command(basecommands.start_plugin(plugin))
        return res.result

    def stop_plugin(self, plugin: str):
        """Stop a plugin"""
        res = self.perform_command(basecommands.stop_plugin(plugin))
        return res.result

    def sync_machine_model(self):
        """
        Wait for the full object model to be updated from RepRapFirmware.

        Deprecated: use sync_object_model instead
        """
        return self.sync_object_model()

    def sync_object_model(self):
        """Wait for the full object model to be updated from RepRapFirmware"""
        return self.perform_command(basecommands.sync_object_model())

    def uninstall_plugin(self, plugin: str):
        """Uninstall a plugin"""
        res = self.perform_command(basecommands.uninstall_plugin(plugin))
        return res.result

    def unlock_machine_model(self):
        """
        Unlock the object model again.

        Deprecated: use unlock_object_model instead
        """
        return self.unlock_object_model()

    def unlock_object_model(self):
        """Unlock the object model again"""
        return self.perform_command(basecommands.unlock_object_model())

    def write_message(
        self,
        message_type: MessageType,
        message: str,
        output_message: bool,
        log_level: LogLevel,
    ):
        """Write an arbitrary message"""
        res = self.perform_command(
            basecommands.write_message(message_type, message, output_message, log_level)
        )
        return res.result


class CommandConnection(BaseCommandConnection):
    """Connection class for sending commands to the control server"""

    def connect(self, socket_file: str = SOCKET_FILE):  # type: ignore
        """Establishes a connection to the given UNIX socket file"""
        return super().connect(clientinitmessages.command_init_message(), socket_file)


class InterceptConnection(BaseCommandConnection):
    """Connection class for intercepting G/M/T-codes from the control server"""

    def __init__(
        self,
        interception_mode: clientinitmessages.InterceptionMode,
        channels=None,
        filters=None,
        priority_codes: bool = False,
        debug: bool = False,
    ):
        super().__init__(debug)
        self.interception_mode = interception_mode
        if channels is not None:
            self.channels = channels
        else:
            self.channels = codechannel.CodeChannel.list()
        self.filters = filters
        self.priority_codes = priority_codes

    def connect(self, socket_file: str = SOCKET_FILE):  # type: ignore
        """Establishes a connection to the given UNIX socket file"""
        iim = clientinitmessages.intercept_init_message(
            self.interception_mode, self.channels, self.filters, self.priority_codes
        )

        return super().connect(iim, socket_file)

    def receive_code(self) -> code.Code:
        """Wait for a code to be intercepted and read it"""
        return self.receive(code.Code)

    def cancel_code(self):
        """Instruct the control server to cancel the last received code (in intercepting mode)"""
        self.send(basecommands.cancel())

    def ignore_code(self):
        """Instruct the control server to ignore the last received code (in intercepting mode)"""
        self.send(basecommands.ignore())

    def resolve_code(
        self, rtype: MessageType = MessageType.Success, content: Optional[str] = None
    ):
        """
        Instruct the control server to resolve the last received code with the given
        message details (in intercepting mode)
        """
        self.send(basecommands.resolve_code(rtype, content))


class SubscribeConnection(BaseConnection):
    """Connection class for subscribing to model updates"""

    def __init__(
        self,
        subscription_mode: clientinitmessages.SubscriptionMode,
        filter_str: str = "",
        filter_list=None,
        debug: bool = False,
    ):
        super().__init__(debug)
        self.subscription_mode = subscription_mode
        self.filter_str = filter_str
        self.filter_list = filter_list

    def connect(self, socket_file: str = SOCKET_FILE):  # type: ignore
        """Establishes a connection to the given UNIX socket file"""
        sim = clientinitmessages.subscribe_init_message(
            self.subscription_mode, self.filter_str, self.filter_list
        )
        return super().connect(sim, socket_file)

    def get_machine_model(self) -> MachineModel:
        """
        Retrieves the full object model of the machine
        In subscription mode this is the first command that has to be called once a
        ConnectionAbortedError has been established.
        """
        machine_model = self.receive(MachineModel)
        self.send(basecommands.acknowledge())
        return machine_model

    def get_serialized_machine_model(self) -> str:
        """
        Optimized method to query the machine model UTF-8 JSON in any mode.
        May be used to get machine model patches as well.
        """
        machine_model_json = self.receive_json()
        self.send(basecommands.acknowledge())
        return machine_model_json

    def get_machine_model_patch(self) -> str:
        """
        Receive a (partial) machine model update.
        If the subscription mode is set to SubscriptionMode.PATCH new update patches of
        the object model need to be applied manually. This method is intended to receive
        such fragments.
        """
        patch_json = self.receive_json()
        self.send(basecommands.acknowledge())
        return patch_json
