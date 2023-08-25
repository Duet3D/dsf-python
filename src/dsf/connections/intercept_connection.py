from typing import List, Optional

from .base_command_connection import BaseCommandConnection
from .init_messages import client_init_messages
from .. import commands, SOCKET_FILE
from ..commands.code_channel import CodeChannel
from ..object_model.messages import MessageType


class InterceptConnection(BaseCommandConnection):
    """Connection class for intercepting G/M/T-codes from the control server"""

    def __init__(
        self,
        interception_mode: client_init_messages.InterceptionMode,
        channels: List[CodeChannel] = None,
        filters: List[str] = None,
        auto_flush: bool = True,
        priority_codes: bool = False,
        debug: bool = False,
    ):
        super().__init__(debug)
        self.interception_mode = interception_mode
        self.channels = channels if channels is not None else CodeChannel.list()
        self.filters = filters
        self.auto_flush = auto_flush
        self.priority_codes = priority_codes

    def connect(self, socket_file: str = SOCKET_FILE):  # noqa
        """Establishes a connection to the given UNIX socket file"""
        iim = client_init_messages.intercept_init_message(
            self.interception_mode, self.channels, self.filters, self.priority_codes, self.auto_flush
        )
        return super().connect(iim, socket_file)

    def receive_code(self) -> commands.code.Code:
        """Wait for a code to be intercepted and read it"""
        return self.receive(commands.code.Code)

    def cancel_code(self):
        """Instruct the control server to cancel the last received code (in intercepting mode)"""
        self.send(commands.code_interception.cancel())

    def ignore_code(self):
        """Instruct the control server to ignore the last received code (in intercepting mode)"""
        self.send(commands.code_interception.ignore())

    def resolve_code(self, rtype: MessageType = MessageType.Success, content: Optional[str] = None):
        """
        Instruct the control server to resolve the last received code with the given
        message details (in intercepting mode)
        """
        self.send(commands.code_interception.resolve_code(rtype, content))
