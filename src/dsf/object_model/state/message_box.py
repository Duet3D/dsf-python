from enum import IntEnum
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


class MessageBox(ModelObject):
    """Information about the message box to show"""
    def __init__(self):
        super(MessageBox, self).__init__()
        # Bitmap of the axis movement controls to show (indices)
        self._axis_controls = 0
        # Content of the message box
        self._message = ""
        # Mode of the message box to display
        self._mode = MessageBoxMode.OkOnly
        # Sequence number of the message box
        self._seq = -1
        # Total timeout for this message box (in ms)
        self._timeout = 0
        # Title of the message box
        self._title = ""
        
    @property
    def axis_controls(self) -> int:
        """Bitmap of the axis movement controls to show (indices)"""
        return self._axis_controls
    
    @axis_controls.setter
    def axis_controls(self, value):
        self._axis_controls = int(value) if value is not None else 0
        
    @property
    def message(self) -> str:
        """Content of the message box"""
        return self._message
    
    @message.setter
    def message(self, value):
        self._message = str(value)
        
    @property
    def mode(self) -> MessageBoxMode:
        """Mode of the message box to display"""
        return self._mode
    
    @mode.setter
    def mode(self, value):
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
    def seq(self, value):
        self._seq = int(value) if value is not None else -1
        
    @property
    def timeout(self) -> int:
        """Total timeout for this message box (in ms)"""
        return self._timeout
    
    @timeout.setter
    def timeout(self, value):
        self._timeout = int(value) if value is not None else 0
        
    @property
    def title(self) -> str:
        """Title of the message box"""
        return self._title
    
    @title.setter
    def title(self, value):
        self._title = str(value)
