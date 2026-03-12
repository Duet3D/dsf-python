import dateutil.parser as dp
from datetime import datetime
from enum import IntEnum

from ..model_object import ModelObject


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

    @classmethod
    def from_json(cls, data: dict[str, object] | str) -> "Message":
        """Deserialize an instance of this class from JSON deserialized dictionary"""
        if isinstance(data, str):
            raise TypeError("Message.from_json expects a decoded JSON dictionary")
        data = dict(data)
        data['msg_type'] = data.pop('type')  # Replace 'type' to not shadow the built-in keyword name
        msg_type = data.get("msg_type", MessageType.Success)
        if isinstance(msg_type, int):
            msg_type = MessageType(msg_type)
        elif not isinstance(msg_type, MessageType):
            msg_type = MessageType.Success
        time_value = data.get("time", datetime.now())
        if isinstance(time_value, str):
            time_value = dp.isoparse(time_value)
        elif not isinstance(time_value, datetime):
            time_value = datetime.now()
        return cls(msg_type=msg_type, content=str(data.get("content", "")), time=time_value)

    def __init__(self, msg_type: MessageType = MessageType.Success, content: str = "", time: datetime = datetime.now()) -> None:
        super().__init__()
        self._content: str = content
        self._time: datetime = time
        self._type: MessageType = msg_type

    def __repr__(self) -> str:
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
    def content(self, value: str):
        self._content = str(value)

    @property
    def time(self) -> datetime:
        """Time at which the message was generated"""
        return self._time

    @time.setter
    def time(self, value: datetime | str):
        if isinstance(value, datetime):
            self._time = value
        elif isinstance(value, str):  # Update from JSON
            self._time = dp.isoparse(value)
        else:
            raise TypeError(f"{__name__}.time must be of type datetime. Got {type(value)}: {value}")

    @property
    def type(self) -> MessageType:
        """Type of this message"""
        return self._type

    @type.setter
    def type(self, value: MessageType | int):
        if isinstance(value, MessageType):
            self._type = value
        elif isinstance(value, int):
            self._type = MessageType(value)
        else:
            raise TypeError(f"{__name__}.type must be of type MessageType. Got {type(value)}: {value}")
