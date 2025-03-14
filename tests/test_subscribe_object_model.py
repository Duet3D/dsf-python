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

from tests.utils import check_json
from src.dsf import PROTOCOL_VERSION
from src.dsf.connections import SubscribeConnection, SubscriptionMode


class TestSubscribeObjectModel(unittest.TestCase):
    """Test suite for the object model subscription example."""

    def setUp(self):
        """Set up test environment before each test."""
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.mock_dcs_socket_file = os.path.join(self.tmp_dir.name, "dsf.socket")

        # Events for synchronization between test and mock server
        self.dcs_passed = threading.Event()
        self.server_ready = threading.Event()

        # Standard responses
        self.success_response = b'{"success":true}'
        self.acknowledge_response = b'{"command":"Acknowledge"}'

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
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
                server.bind(self.mock_dcs_socket_file)
                server.listen(1)
                server.settimeout(5)
                self.server_ready.set()

                conn, _ = server.accept()
                with conn:
                    # Initial handshake
                    conn.sendall(f'{{"version":{PROTOCOL_VERSION}, "id":"foobar"}}'.encode())

                    # Verify subscription setup
                    setup_msg = conn.recv(1024)
                    expected_setup = {
                        "mode": "Subscribe",
                        "version": PROTOCOL_VERSION,
                        "subscriptionMode": "Patch",
                        "filter": "",
                        "filters": None
                    }
                    check_json(expected_setup, setup_msg.decode())

                    # Connection setup response
                    conn.sendall(self.success_response)

                    # Process model data and updates
                    model_updates = [
                        "tests/object_model/model_full.json",
                        "tests/object_model/model_update.json",
                        # "tests/object_model/model_update_heat.json",
                        # "tests/object_model/model_update_sensors_state.json"
                    ]

                    for model_file in model_updates:
                        # Send model data
                        with open(model_file, 'r') as f:
                            update_data = json.load(f)
                        conn.sendall(json.dumps(update_data).encode())

                        # Verify acknowledge response
                        ack = conn.recv(1024)
                        self.assertEqual(ack, self.acknowledge_response,
                                         f"Expected acknowledge command, received: {ack.decode()}")

            self.dcs_passed.set()  # Test completed successfully

        except Exception as e:
            print(f"Mock DCS server error: {e}")
            # Don't set dcs_passed if there was an exception

    def test_subscribe_object_model(self):
        """Test the subscribe_object_model example."""
        # Execute the example code
        subscribe_connection = SubscribeConnection(SubscriptionMode.PATCH)
        subscribe_connection.connect(self.mock_dcs_socket_file)

        # Get the complete model once
        om = subscribe_connection.get_object_model()
        self.assertEqual(om.boards[0].name, "Duet 3 MB6HC")
        self.assertEqual(len(om.boards), 8)

        # Get boards patch
        # This should remove 1 of the boards
        update = subscribe_connection.get_object_model_patch()
        om.update_from_json(update)
        self.assertEqual(len(om.boards), 7)
        self.assertEqual(om.boards[3].drivers[0].closed_loop.position_error.max, 0.085)

        # # Get heat patch
        # update = subscribe_connection.get_object_model_patch()
        # om.update_from_json(update)

        # # Get sensors state patch
        # update = subscribe_connection.get_object_model_patch()
        # om.update_from_json(update)

        subscribe_connection.close()

        # Wait for the mock DCS to complete
        self.server_thread.join(timeout=5)

        # Verify the test completed successfully
        self.assertTrue(self.dcs_passed.is_set(), "The mock DCS did not complete successfully")


if __name__ == "__main__":
    unittest.main()
