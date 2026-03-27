from .spindle_state import SpindleState
from .spindle_type import SpindleType
from ..model_object import ModelObject
from ..utils import nullable_model_prop, model_prop


class Spindle(ModelObject):
    """Information about a CNC spindles"""

    # Active RPM
    active = nullable_model_prop("active", int)

    # Flags whether the spindles may spin in reverse direction
    can_reverse = nullable_model_prop("can_reverse", bool)

    # Current RPM, negative if anticlockwise direction
    current = nullable_model_prop("current", int)

    # Frequency (in Hz)
    frequency = nullable_model_prop("frequency", int)

    # Idle PWM value (0..1)
    idle_pwm = nullable_model_prop("idle_pwm", float)

    # Maximum RPM
    max = nullable_model_prop("max", int)

    # Maximum PWM value when turned on (0..1)
    max_pwm = nullable_model_prop("max_pwm", float)

    # Minimum RPM when turned on
    min = nullable_model_prop("min", int)

    # Minimum PWM value when turned on (0..1)
    min_pwm = nullable_model_prop("min_pwm", float)

    # Current state
    state = model_prop("state", SpindleState, SpindleState.unconfigured)

    # Spindle type
    type = nullable_model_prop("type", SpindleType, lambda: None)

    def __init__(self):
        super().__init__()
