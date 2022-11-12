from .base_command_connection import BaseCommandConnection
from .init_messages import client_init_messages
from .. import SOCKET_FILE


class CommandConnection(BaseCommandConnection):
    """Connection class for sending commands to the control server"""

    def connect(self, socket_file: str = SOCKET_FILE):  # type: ignore
        """Establishes a connection to the given UNIX socket file"""
        return super().connect(client_init_messages.command_init_message(), socket_file)
