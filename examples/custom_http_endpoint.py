#!/usr/bin/env python3

"""
Example of custom HTTP endpoints served by this script through DSF

    GET  http://duet3.local/machine/example/hello?name=Duet  Reply with plain text
    POST http://duet3.local/machine/example/echo             Reply with the JSON body that was sent

Try it with:
    curl "http://duet3.local/machine/example/hello?name=Duet"
    curl -X POST -d '{"answer": 42}' http://duet3.local/machine/example/echo

Make sure when running this script to have access to the DSF UNIX socket owned by the dsf user.
"""

import json
import time
from typing import Any

from dsf.connections import CommandConnection
from dsf.http import HttpCallback, HttpEndpointConnection, HttpEndpointUnixSocket, HttpResponseType, ReceivedHttpRequest
from dsf.object_model import HttpEndpointType


async def hello(connection: HttpEndpointConnection) -> None:
    request: ReceivedHttpRequest = await connection.read_request()
    # Query parameters are available as a dictionary
    name: str = request.queries.get("name", "world")
    # The connection is closed automatically once the response is sent
    await connection.send_response(200, f"Hello {name}!", HttpResponseType.PlainText)


async def echo(connection: HttpEndpointConnection) -> None:
    request: ReceivedHttpRequest = await connection.read_request()
    try:
        data: Any = json.loads(request.body)
    except json.JSONDecodeError:
        await connection.send_response(400, "Body must be valid JSON", HttpResponseType.PlainText)
        return
    response: dict[str, Any] = {"received": data, "sessionId": request.session_id}
    await connection.send_response(200, json.dumps(response), HttpResponseType.JSON)


def custom_http_endpoints() -> None:
    command_connection: CommandConnection = CommandConnection()
    command_connection.connect()
    endpoints: list[HttpEndpointUnixSocket] = []

    try:
        # Register each endpoint with DSF and attach a handler to process its requests.
        # Handlers are run in the background so this script is free to do other work
        routes: list[tuple[HttpEndpointType, str, HttpCallback]] = [
            (HttpEndpointType.GET, "hello", hello),
            (HttpEndpointType.POST, "echo", echo),
        ]
        for endpoint_type, path, handler in routes:
            endpoint: HttpEndpointUnixSocket = command_connection.add_http_endpoint(endpoint_type, "example", path)
            endpoint.set_endpoint_handler(handler)
            endpoints.append(endpoint)

        print("Endpoints are available at /machine/example/hello and /machine/example/echo")
        print("Press Ctrl+C to stop")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the endpoints from DSF and close their sockets
        for endpoint in endpoints:
            command_connection.remove_http_endpoint(endpoint.endpoint_type, endpoint.namespace, endpoint.endpoint_path)
            endpoint.close()
        command_connection.close()


if __name__ == "__main__":
    custom_http_endpoints()
