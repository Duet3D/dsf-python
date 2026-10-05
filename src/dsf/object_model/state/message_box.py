from enum import IntEnum

from ...utils import DeprecatedAliasEnumType
from ..model_object import ModelObject
from ..model_collection import ModelCollection
from ..utils import model_prop, nullable_model_prop


class MessageBoxMode(IntEnum, metaclass=DeprecatedAliasEnumType):
    """Supported modes of displaying a message box"""

    # Display a message box without any buttons
    NO_BUTTONS = 0

    # Display a message box with only a Close button
    CLOSE_ONLY = 1

    # Display a message box with only an Ok button which is supposed to send M292 when pressed
    OK_ONLY = 2

    # Display a message box with an Ok button that sends M292 P0 or a cancel button that sends M292 P1 when clicked
    OK_CANCEL = 3

    # Multiple choices, blocking
    MULTIPLE_CHOICE = 4

    # Integer value required, blocking
    INT_INPUT = 5

    # Floating-point value required, blocking
    FLOAT_INPUT = 6

    # String value required, blocking
    STRING_INPUT = 7

    # Previous names, deprecated
    CloseOnly = CLOSE_ONLY
    FloatInput = FLOAT_INPUT
    IntInput = INT_INPUT
    MultipleChoice = MULTIPLE_CHOICE
    NoButtons = NO_BUTTONS
    OkCancel = OK_CANCEL
    OkOnly = OK_ONLY
    StringInput = STRING_INPUT


class MessageBox(ModelObject):
    """Information about the message box to show"""

    axis_controls = nullable_model_prop("axis_controls", int)
    cancel_button = model_prop("cancel_button", bool, False)
    choices = nullable_model_prop("choices", ModelCollection[str], lambda: ModelCollection(str))
    default = nullable_model_prop("default", object)
    max = nullable_model_prop("max", float)
    message = model_prop("message", str, "")
    min = nullable_model_prop("min", float)
    mode = model_prop("mode", MessageBoxMode, MessageBoxMode.OK_ONLY)
    seq = model_prop("seq", int, -1)
    timeout = model_prop("timeout", int, 0)
    title = model_prop("title", str, "")

    def __init__(self):
        super(MessageBox, self).__init__()
