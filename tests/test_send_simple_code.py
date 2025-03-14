import unittest
from unittest.mock import patch
import threading
import os
import pathlib
import socket
import tempfile
import time
import importlib.util
import json

from src.dsf import PROTOCOL_VERSION
from src.dsf.connections import CommandConnection
from tests.utils import check_json


class TestSendSimpleCode(unittest.TestCase):
    """Test suite for the send simple code example."""

    def setUp(self):
        """Set up test environment before each test."""
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.mock_dcs_socket_file = os.path.join(self.tmp_dir.name, "dsf.socket")

        # Events for synchronization between test and mock server
        self.dcs_passed = threading.Event()
        self.server_ready = threading.Event()

        # Start mock server
        self.server_thread = threading.Thread(target=self._run_mock_dcs_server, daemon=True)
        self.server_thread.start()

        # Wait for server to be ready
        self.assertTrue(self.server_ready.wait(timeout=5), "Mock DCS server failed to start")

    def tearDown(self):
        """Clean up after test."""
        if self.server_thread.is_alive():
            self.server_thread.join(timeout=1)

        self.tmp_dir.cleanup()

    def _run_mock_dcs_server(self):
        """Run mock DCS server to simulate socket communication."""
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.mock_dcs_socket_file)
        server.listen(1)
        self.server_ready.set()

        # Set a timeout for accepting connections
        server.settimeout(5)
        conn, _ = server.accept()
        conn.settimeout(5)

        try:
            with conn:
                # Initial handshake - send version and ID
                conn.sendall(f'{{"version":{PROTOCOL_VERSION}, "id":"foobar"}}'.encode())

                # Receive and verify the command setup message
                setup_msg = conn.recv(1024)
                expected_setup = f'{{"mode":"Command","version":{PROTOCOL_VERSION}}}'
                self.assertEqual(setup_msg.decode(), expected_setup, f"Incorrect setup message: {setup_msg.decode()}")

                # Send success response for connection setup
                conn.sendall('{"success":true}'.encode())

                # Receive and verify the SimpleCode command
                cmd_msg = conn.recv(1024)
                expected_cmd = {
                    "command": "SimpleCode",
                    "code": "echo \"Hello world!\"",
                    "channel": "SBC", "executeAsynchronously": False
                }
                self.assertEqual(json.loads(cmd_msg.decode()), expected_cmd,
                                 f"Incorrect command message: {cmd_msg.decode()}")

                # Send success response for the command
                conn.sendall('{"result":"Hello world!", "success":true}'.encode())

                self.dcs_passed.set()  # indicate that all asserts passed
        except AssertionError as e:
            print(f"Assertion error: {e}")
            self.dcs_passed.clear()  # indicate that an assert failed

    def test_send_simple_code(self):
        """Test the send_simple_code example."""
        # Execute the example code we're testing
        command_connection = CommandConnection(debug=True)
        command_connection.connect(self.mock_dcs_socket_file)

        # res = command_connection.set_plugin_data("ExecOnMcode", "test", "1")
        # Perform a simple command and wait for its output
        res = command_connection.perform_simple_code("echo \"Hello world!\"")
        self.assertEqual(res, "Hello world!")
        command_connection.close()

        # Wait for the mock DCS to complete with a timeout
        self.server_thread.join(timeout=5)

        # Verify the test completed successfully
        self.assertTrue(self.dcs_passed.is_set(), "The mock DCS did not complete successfully")


if __name__ == "__main__":
    unittest.main()
