from enum import IntEnum
from typing import List, Union
from ..model_object import ModelObject


class MessageBoxMode(IntEnum):
    """Supported modes of displaying a message box"""

    # Display a message box without any buttons
    NoButtons = 0

    # Display a message box with only a Close button
    CloseOnly = 1

    # Display a message box with only an Ok button which is supposed to send M292 when pressed
    OkOnly = 2

    # Display a message box with an Ok button that sends M292 P0 or a cancel button that sends M292 P1 when clicked
    OkCancel = 3

    # Multiple choices, blocking
    MultipleChoice = 4

    # Integer value required, blocking
    IntInput = 5

    # Floating-point value required, blocking
    FloatInput = 6

    # String value required, blocking
    StringInput = 7


class MessageBox(ModelObject):
    """Information about the message box to show"""

    def __init__(self) -> None:
        super(MessageBox, self).__init__()
        # Bitmap of the axis movement controls to show (indices)
        self._axis_controls: Union[int, None] = None
        # Indicates if a cancel button is supposed to be shown
        self._cancel_button: bool = False
        # List of possible choices (only for mode 4)
        self._choices: Union[List[str], None] = []
        # Default value (only for modes >= 4)
        self._default: bool | float | int | str | None = None
        # Maximum input value (only for modes >= 5)
        self._max: Union[float, None] = None
        # Content of the message box
        self._message: str = ""
        # Minimum input value (only for modes >= 5)
        self._min: Union[float, None] = None
        # Mode of the message box to display
        self._mode: MessageBoxMode = MessageBoxMode.OkOnly
        # Sequence number of the message box
        self._seq: int = -1
        # Total timeout for this message box (in ms)
        self._timeout: int = 0
        # Title of the message box
        self._title: str = ""

    @property
    def axis_controls(self) -> Union[int, None]:
        """Bitmap of the axis movement controls to show (indices)"""
        return self._axis_controls

    @axis_controls.setter
    def axis_controls(self, value: int | str | None):
        self._axis_controls = int(value) if value is not None else None

    @property
    def cancel_button(self) -> bool:
        """Indicates if a cancel button is supposed to be shown"""
        return self._cancel_button

    @cancel_button.setter
    def cancel_button(self, value: bool | int | str):
        self._cancel_button = bool(value)

    @property
    def choices(self) -> Union[List[str], None]:
        """List of possible choices (only for mode 4)"""
        return self._choices

    @choices.setter
    def choices(self, value: list[object] | None):
        self._choices = [str(v) for v in value] if value is not None else None

    @property
    def default(self) -> bool | float | int | str | None:
        """Default value (only for modes >= 4)"""
        return self._default

    @default.setter
    def default(self, value: bool | float | int | str | None):
        self._default = value

    @property
    def max(self) -> Union[float, None]:
        """Maximum input value (only for modes >= 5)"""
        return self._max

    @max.setter
    def max(self, value: float | int | str | None):
        self._max = float(value) if value is not None else None
        
    @property
    def message(self) -> str:
        """Content of the message box"""
        return self._message
    
    @message.setter
    def message(self, value: str):
        self._message = str(value)

    @property
    def min(self) -> Union[float, None]:
        """Minimum input value (only for modes >= 5)"""
        return self._min

    @min.setter
    def min(self, value: float | int | str | None):
        self._min = float(value) if value is not None else None
        
    @property
    def mode(self) -> MessageBoxMode:
        """Mode of the message box to display"""
        return self._mode
    
    @mode.setter
    def mode(self, value: MessageBoxMode | int | str | None):
        if value is None:
            self._mode = MessageBoxMode.OkOnly
        elif isinstance(value, MessageBoxMode):
            self._mode = value
        elif isinstance(value, int):
            self._mode = MessageBoxMode(value)
        elif isinstance(value, str):
            self._mode = MessageBoxMode[value]
        else:
            raise TypeError(f"{__name__}.mode must be of type MessageBoxMode. Got {type(value)}: {value}")
        
    @property
    def seq(self) -> int:
        """Sequence number of the message box
        This is increased whenever a new message box is supposed to be displayed"""
        return self._seq
    
    @seq.setter
    def seq(self, value: int | str):
        self._seq = int(value)
        
    @property
    def timeout(self) -> int:
        """Total timeout for this message box (in ms)"""
        return self._timeout
    
    @timeout.setter
    def timeout(self, value: int | str):
        self._timeout = int(value)
        
    @property
    def title(self) -> str:
        """Title of the message box"""
        return self._title
    
    @title.setter
    def title(self, value: str):
        self._title = str(value)
