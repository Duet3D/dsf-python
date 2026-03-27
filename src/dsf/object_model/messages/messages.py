import dateutil.parser as dp
from datetime import datetime
from enum import IntEnum

from ..model_object import ModelObject
from ..utils import model_prop


class MessageType(IntEnum):
    """Type of generic message"""

    # This is a success message
    Success = 0

    # This is a warning message
    Warning = 1

    # This is an error message
    Error = 2


class Message(ModelObject):
    """
    Generic container for messages
    :param content: Content of this message
    :param time: Time at which the message was generated
    :param msg_type: Type of this message
    """

    # Content of this message
    content = model_prop("content", str, "")

    # Time at which the message was generated
    time = model_prop("time", datetime, datetime.now)

    # Type of this message
    type = model_prop("type", MessageType, MessageType.Success)

    def __init__(self, msg_type: MessageType = MessageType.Success, content: str = "", time: datetime = datetime.now()):
        super().__init__()
        self.content = content
        self.time = time
        self.type = msg_type

    def __repr__(self):
        if self.type == MessageType.Error:
            return f"Error: {self.content}"
        elif self.type == MessageType.Warning:
            return f"Warning: {self.content}"
        else:
            return f"{self.content}"
