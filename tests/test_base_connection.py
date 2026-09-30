import socket
import time
import unittest
from unittest.mock import Mock, patch

from src.dsf.connections.base_connection import BaseConnection


class TestBaseConnection(unittest.TestCase):
    def test_has_data_available_returns_true_for_complete_buffered_json(self):
        connection = BaseConnection()
        connection.input = '{"key":1}'

        self.assertTrue(connection.has_data_available())

    def test_has_data_available_returns_false_for_partial_buffer_without_socket_data(self):
        connection = BaseConnection()
        connection.input = '{"key"'
        connection.socket = Mock(spec=socket.socket)

        with patch("src.dsf.connections.base_connection.select.select", return_value=([], [], [])):
            self.assertFalse(connection.has_data_available())

    def test_has_data_available_returns_true_when_socket_is_readable(self):
        connection = BaseConnection()
        connection.socket = Mock(spec=socket.socket)

        with patch(
            "src.dsf.connections.base_connection.select.select",
            return_value=([connection.socket], [], []),
        ):
            self.assertTrue(connection.has_data_available())

    def test_receive_json_returns_first_complete_object_and_buffers_the_rest(self):
        connection = BaseConnection()
        client, server = socket.socketpair()
        with client, server:
            connection.socket = client
            server.sendall(b'{"key":1}{"key"')

            self.assertEqual(connection.receive_json(), '{"key":1}')
            self.assertEqual(connection.input, '{"key"')

    def test_receive_json_raises_when_server_closes_connection(self):
        connection = BaseConnection(timeout=30)
        client, server = socket.socketpair()
        with client:
            connection.socket = client
            server.close()

            start = time.monotonic()
            self.assertRaises(ConnectionError, connection.receive_json)
            # Must fail immediately instead of waiting for the timeout
            self.assertLess(time.monotonic() - start, 5)


if __name__ == "__main__":
    unittest.main()
