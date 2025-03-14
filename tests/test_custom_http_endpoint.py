import threading
import os
import pathlib
import socket
import time
import importlib.util
import unittest
import json
import tempfile
import requests

from src.dsf import PROTOCOL_VERSION
from src.dsf.connections import CommandConnection
from src.dsf.http import HttpEndpointConnection, HttpResponseType
from src.dsf.object_model import HttpEndpointType


# async def respond_something(http_endpoint_connection: HttpEndpointConnection):
#     r = await http_endpoint_connection.read_request()
#     if (len(r.body) > 0):
#         data = json.loads(r.body)
#     await http_endpoint_connection.send_response(200, "so happy you asked for it!", HttpResponseType.PlainText)
#     http_endpoint_connection.close()


class TestCustomHttpEndpoint(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.temp_dir = tempfile.TemporaryDirectory()
        self.mock_dcs_socket_file = os.path.join(self.temp_dir.name, "dsf.socket")

        # Set up the threading event for synchronization
        self.dcs_passed = threading.Event()
        self.server_ready = threading.Event()

        # Start the mock DCS server in a separate thread
        self.server_thread = threading.Thread(target=self.mock_dcs, daemon=True)
        self.server_thread.start()

        # Wait for server to be ready
        self.assertTrue(self.server_ready.wait(timeout=5), "Mock DCS server failed to start")

    def tearDown(self):
        # Clean up resources
        if self.server_thread.is_alive():
            self.server_thread.join(timeout=1)
        self.temp_dir.cleanup()

    def mock_dcs(self):
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.mock_dcs_socket_file)
        server.listen(1)
        self.server_ready.set()

        conn, _ = server.accept()
        conn.sendall(f'{{"version":{PROTOCOL_VERSION}, "id":"foobar"}}'.encode())

        setup_msg = conn.recv(1024)
        self.assertEqual(json.loads(setup_msg.decode()), {"mode": "Command", "version": PROTOCOL_VERSION})

        conn.sendall('{"success":true}'.encode())

        http_endpoint_msg = conn.recv(1024)
        self.assertEqual(
            json.loads(http_endpoint_msg.decode()), {
                "command": "AddHttpEndpoint",
                "endpointType": "GET",
                "namespace": "custom",
                "path": "getIt",
                "isUploadRequest": False
            }
        )

        conn.sendall('{"result":"/var/run/dsf/custom/getIt-GET.sock","success":true}'.encode())
        conn.close()
        self.dcs_passed.set()  # indicate that all asserts passed and the mock_dcs is shutting down

    def test_custom_http_endpoint(self):
        # Call the function that creates the custom HTTP endpoint
        cmd_conn = CommandConnection(debug=True)
        cmd_conn.connect(self.mock_dcs_socket_file)

        # Setup the endpoint
        endpoint = cmd_conn.add_http_endpoint(HttpEndpointType.GET, "custom", "getIt")

        # Register our handler to reply on requests
        # endpoint.set_endpoint_handler(respond_something)

        # Wait for mock DCS server to complete
        self.server_thread.join(timeout=1)

        time.sleep(1)

        if endpoint is not None:
            endpoint.close()
        cmd_conn.close()

        # Verify the test completed successfully
        self.assertTrue(self.dcs_passed.is_set(), "The mock DCS did not complete successfully")


if __name__ == "__main__":
    unittest.main()
