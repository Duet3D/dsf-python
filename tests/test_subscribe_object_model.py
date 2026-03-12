import unittest
from unittest.mock import ANY
import threading
import os
import socket
import tempfile
import time
import json
from typing import Any, cast

from tests.utils import check_json
from src.dsf import PROTOCOL_VERSION
from src.dsf.connections import SubscribeConnection, SubscriptionMode


class TestSubscribeObjectModel(unittest.TestCase):
    """Test suite for the object model subscription example."""

    @staticmethod
    def _wait_for_data_available(subscribe_connection: SubscribeConnection, timeout: float = 1.0) -> bool:
        deadline = time.time() + timeout
        while time.time() < deadline:
            if subscribe_connection.has_data_available():
                return True
            time.sleep(0.01)
        return False

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
                    expected_setup: dict[str, Any] = {
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
        board = om.boards[0]
        self.assertIsNotNone(board)
        assert board is not None
        self.assertEqual(board.name, "Duet 3 MB6HC")
        self.assertEqual(len(om.boards), 8)

        # Get boards patch
        # This should remove 1 of the boards
        update = subscribe_connection.get_object_model_patch()
        om.update_from_json(update)
        boards = cast(list[Any], om.boards)
        self.assertEqual(len(boards), 7)
        self.assertIsNotNone(boards[3])
        board = boards[3]
        assert board is not None
        self.assertIsNotNone(board.drivers)
        drivers = cast(list[Any], board.drivers)
        self.assertIsNotNone(drivers[0])
        driver = drivers[0]
        assert driver is not None
        closed_loop = driver.closed_loop
        self.assertIsNotNone(closed_loop)
        assert closed_loop is not None
        self.assertEqual(closed_loop.position_error.max, 0.085)

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

    def test_has_data_available_during_subscription_flow(self):
        """Test that has_data_available reflects queued model and patch updates."""
        subscribe_connection = SubscribeConnection(SubscriptionMode.PATCH)
        subscribe_connection.connect(self.mock_dcs_socket_file)

        self.assertTrue(
            self._wait_for_data_available(subscribe_connection),
            "Expected the initial object model to be readable",
        )

        subscribe_connection.get_object_model()

        self.assertTrue(
            self._wait_for_data_available(subscribe_connection),
            "Expected the next object model patch to be readable after acknowledge",
        )

        subscribe_connection.get_object_model_patch()

        self.assertFalse(subscribe_connection.has_data_available())

        subscribe_connection.close()

        self.server_thread.join(timeout=5)
        self.assertTrue(self.dcs_passed.is_set(), "The mock DCS did not complete successfully")

    def test_subscribe_to_keys_runs_callback_for_matching_changes(self):
        """Test that subscribe_to_keys invokes callbacks synchronously for matching patch keys."""
        subscribe_connection = SubscribeConnection(SubscriptionMode.PATCH)
        subscribe_connection.connect(self.mock_dcs_socket_file)

        try:
            subscribe_connection.get_object_model()

            callback_changes: list[tuple[str, object, tuple[int, ...] | None]] = []

            def record_change(*, key: str, data: object, indices: tuple[int, ...] | None) -> None:
                callback_changes.append((key, data, indices))

            unsubscribe = subscribe_connection.subscribe_to_keys(
                ["boards", "heat.heaters.0.current", "state.upTime"],
                record_change,
            )

            self.assertTrue(
                self._wait_for_data_available(subscribe_connection),
                "Expected the next object model patch to be readable",
            )
            subscribe_connection.get_object_model()

            self.assertEqual(len(callback_changes), 3)
            self.assertIn(("heat.heaters.0.current", 16.22, None), callback_changes)
            self.assertIn(("state.upTime", 3658, None), callback_changes)
            self.assertIn(("boards", ANY, None), callback_changes)
            boards_data = next(data for key, data, _ in callback_changes if key == "boards")
            self.assertIsInstance(boards_data, list)
            self.assertEqual(len(cast(list[Any], boards_data)), 7)

            unsubscribe()
        finally:
            subscribe_connection.close()

        self.server_thread.join(timeout=5)
        self.assertTrue(self.dcs_passed.is_set(), "The mock DCS did not complete successfully")

    def test_subscribe_to_keys_passes_wildcard_indexes(self):
        """Test that ^ wildcard key paths pass the matched list indexes to the callback."""
        subscribe_connection = SubscribeConnection(SubscriptionMode.PATCH)
        subscribe_connection.connect(self.mock_dcs_socket_file)

        try:
            subscribe_connection.get_object_model()

            callback_changes: list[tuple[str, object, tuple[int, ...] | None]] = []

            def record_change(*, key: str, data: object, indices: tuple[int, ...] | None) -> None:
                callback_changes.append((key, data, indices))

            unsubscribe = subscribe_connection.subscribe_to_keys(
                ["heat.heaters.^.current", "sensors.analog.^.lastReading"],
                record_change,
            )

            self.assertTrue(
                self._wait_for_data_available(subscribe_connection),
                "Expected the next object model patch to be readable",
            )
            subscribe_connection.get_object_model()

            self.assertEqual(len(callback_changes), 5)
            self.assertIn(
                ("heat.heaters.^.current", 16.22, (0,)),
                callback_changes,
            )
            self.assertIn(
                ("sensors.analog.^.lastReading", 16.22, (0,)),
                callback_changes,
            )
            self.assertIn(
                ("heat.heaters.^.current", 18.39, (2,)),
                callback_changes,
            )
            self.assertIn(
                ("sensors.analog.^.lastReading", 18.39, (2,)),
                callback_changes,
            )
            self.assertIn(
                ("sensors.analog.^.lastReading", 21.23, (10,)),
                callback_changes,
            )

            unsubscribe()
        finally:
            subscribe_connection.close()

        self.server_thread.join(timeout=5)
        self.assertTrue(self.dcs_passed.is_set(), "The mock DCS did not complete successfully")


if __name__ == "__main__":
    unittest.main()
