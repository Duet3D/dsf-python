from datetime import datetime
from enum import IntEnum


class MessageType(IntEnum):
    """Type of generic message"""

    # This is a success message
    Success = 0

    # This is a warning message
    Warning = 1

    # This is an error message
    Error = 2


class Message:
    """
    Generic container for messages
    :param content: Content of this message
    :param time: Time at which the message was generated
    :param type_: Type of this message
    """

    @classmethod
    def from_json(cls, data):
        """Deserialize an instance of this class from JSON deserialized dictionary"""
        return cls(**data)

    def __init__(self, type_: MessageType = MessageType.Success, content: str = "", time: datetime = datetime.now()):
        super().__init__()
        self._content = content
        self._time = time
        self._type = type_

    def __repr__(self):
        if self.type == MessageType.Error:
            return f"Error: {self.content}"
        elif self.type == MessageType.Warning:
            return f"Warning: {self.content}"
        else:
            return f"{self.content}"

    @property
    def content(self) -> str:
        """Content of this message"""
        return self._content

    @content.setter
    def content(self, value):
        self._content = str(value)

    @property
    def time(self) -> datetime:
        """Time at which the message was generated"""
        return self._time

    @time.setter
    def time(self, value):
        if isinstance(value, datetime):
            self._time = value
        elif isinstance(value, str):  # Update from JSON
            self._time = datetime.fromisoformat(value)
        else:
            raise TypeError(f"{__name__}.time must be of type datetime. Got {type(value)}: {value}")

    @property
    def type(self) -> MessageType:
        """Type of this message"""
        return self._type

    @type.setter
    def type(self, value):
        if not isinstance(value, MessageType):
            raise TypeError(f"{__name__}.type must be of type MessageType. Got {type(value)}: {value}")
        self._type = value
