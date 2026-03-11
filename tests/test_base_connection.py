import unittest
from unittest.mock import patch

from src.dsf.connections.base_connection import BaseConnection


class TestBaseConnection(unittest.TestCase):
    def test_has_data_available_returns_true_for_complete_buffered_json(self):
        connection = BaseConnection()
        connection.input = '{"key":1}'

        self.assertTrue(connection.has_data_available())

    def test_has_data_available_returns_false_for_partial_buffer_without_socket_data(self):
        connection = BaseConnection()
        connection.input = '{"key"'
        connection.socket = object()

        with patch('src.dsf.connections.base_connection.select.select', return_value=([], [], [])):
            self.assertFalse(connection.has_data_available())

    def test_has_data_available_returns_true_when_socket_is_readable(self):
        connection = BaseConnection()
        connection.socket = object()

        with patch(
            'src.dsf.connections.base_connection.select.select',
            return_value=([connection.socket], [], []),
        ):
            self.assertTrue(connection.has_data_available())


if __name__ == '__main__':
    unittest.main()