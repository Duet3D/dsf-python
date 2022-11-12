import asyncio
import json
import os
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

from . import DEFAULT_BACKLOG
from .object_model.http_endpoints import HttpEndpointType


class HttpResponseType(str, Enum):
    """Enumeration of supported HTTP responses"""

    StatusCode = "StatusCode"
    PlainText = "PlainText"
    JSON = "JSON"
    File = "File"


class ReceivedHttpRequest:
    """Notification sent by the webserver when a new HTTP request is received"""

    @classmethod
    def from_json(cls, data):
        """Deserialize an instance of this class from deserialized JSON dictionary"""
        return cls(**data)

    def __init__(self, sessionId: int, queries: dict, headers: dict, contentType: str, body: str):
        self.session_id = sessionId
        self.queries = queries
        self.headers = headers
        self.content_type = contentType
        self.body = body


class HttpEndpointConnection:
    """Connection class for dealing with requests received from a custom HTTP endpoint"""

    def __init__(self, reader, writer, is_websocket: bool, debug: bool = False):
        """Constructor for a new connection dealing with a single HTTP endpoint request"""
        self.reader = reader
        self.writer = writer
        self.is_websocket = is_websocket
        self.debug = debug

    def close(self):
        """Close the connection"""
        self.writer.close()

    async def read_request(self):
        """
        Read information about the last HTTP request.
        Note that a call to this method may fail!
        """
        return await self.receive(ReceivedHttpRequest)

    async def send_response(
        self,
        status_code: int = 204,
        response: str = "",
        response_type: HttpResponseType = HttpResponseType.StatusCode,
    ):
        """
        Send a simple HTTP response to the client and dispose
        this connection unless it is a WebSocket.
        """
        try:
            await self.send(
                {
                    "StatusCode": status_code,
                    "Response": response,
                    "ResponseType": response_type,
                }
            )
        finally:
            # Close this connection automatically if only one response can be sent
            if not self.is_websocket:
                self.close()

    async def receive(self, cls):
        """Receive a deserialized object"""
        json_string = await self.receive_json()
        return cls.from_json(json.loads(json_string))

    async def receive_json(self):
        """Receive a JSON object"""
        json_string = (await self.reader.read(32 * 1024)).decode("utf8")
        if self.debug:
            print("recv:", json_string)
        return json_string

    async def send(self, obj):
        """Send an arbitrary object"""
        json_string = json.dumps(obj, default=lambda o: o.__dict__)
        if self.debug:
            print("send:", json_string)
        self.writer.write(json_string.encode("utf8"))
        await self.writer.drain()


class HttpEndpointUnixSocket:
    """Class for dealing with custom HTTP endpoints"""

    def __init__(
        self,
        endpoint_type: HttpEndpointType,
        namespace: str,
        path: str,
        socket_file: str,
        backlog: int = DEFAULT_BACKLOG,
        debug: bool = False,
    ):
        """Open a new UNIX socket on the given file path"""
        self.endpoint_type = endpoint_type
        self.namespace = namespace
        self.endpoint_path = path
        self.socket_file = socket_file
        self.backlog = backlog
        self.handler = None
        self.debug = debug
        self._loop = None
        self._server = None

        try:
            os.remove(self.socket_file)
        except FileNotFoundError:
            # We don't care if the file was missing
            # TODO: should we care about deletion failed?
            pass

        self.executor = ThreadPoolExecutor(max_workers=1)
        self.event_loop = self.executor.submit(self.start_connection_listener)

    def close(self):
        """Close the socket connection"""
        if self._loop is not None:
            # TODO: this enables correctly ending the loop. Why?
            self._loop.set_debug(True)
            self._server.close()
            self._loop.stop()
        self.event_loop.cancel()
        self.executor.shutdown(wait=False)
        try:
            os.remove(self.socket_file)
        except FileNotFoundError:
            pass

    def set_endpoint_handler(self, handler):
        """Set the handler to handle client connections"""
        self.handler = handler

    def start_connection_listener(self):
        try:
            self._loop = asyncio.new_event_loop()
            self._server = asyncio.start_unix_server(
                self.handle_connection, self.socket_file, backlog=self.backlog
            )
            self._loop.create_task(self._server)
            self._loop.run_forever()
        finally:
            self._loop.close()

    async def handle_connection(self, reader, writer):
        """Handle incoming UNIX socket connections (HTTP/WebSocket requests)"""
        http_endpoint_connection = HttpEndpointConnection(
            reader,
            writer,
            self.endpoint_type == HttpEndpointType.WebSocket,
            debug=self.debug,
        )
        if self.handler is not None:
            # Invoke the event handler and forward the wrapped connection for dealing
            # with a single endpoint connection.
            # Note that the event delegate is responsible for disposing the connection!
            await self.handler(http_endpoint_connection)
        else:
            await http_endpoint_connection.send_response(500, "No event handler registered")
            http_endpoint_connection.close()
