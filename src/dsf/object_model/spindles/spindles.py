from .spindle_state import SpindleState
from .spindle_type import SpindleType
from ..model_object import ModelObject

from typing import Union


class Spindle(ModelObject):
    """Information about a CNC spindles"""

    def __init__(self):
        super().__init__()
        # Active RPM
        self._active = 0
        # Flags whether the spindles may spin in reverse direction
        self._can_reverse = False
        # Current RPM, negative if anticlockwise direction
        self._current = 0
        # Frequency (in Hz)
        self._frequency = 0
        #
        self._idle_pwm = 0
        # Maximum RPM
        self._max = 10000
        #
        self._max_pwm = 1
        # Minimum RPM when turned on
        self._min = 60
        #
        self._min_pwm = 0
        # Current state
        self._state = SpindleState.unconfigured
        # Spindle type
        self._type = SpindleType.null
        
    @property
    def active(self) -> Union[int, None]:
        """Active RPM"""
        return self._active
    
    @active.setter
    def active(self, value: Union[int, None]):
        self._active = None if value is None else int(value)
        
    @property
    def can_reverse(self) -> Union[bool, None]:
        """Flags whether the spindles may spin in reverse direction"""
        return self._can_reverse
    
    @can_reverse.setter
    def can_reverse(self, value: Union[bool, None]):
        self._can_reverse = None if value is None else bool(value)
        
    @property
    def current(self) -> Union[int, None]:
        """Current RPM, negative if anticlockwise direction"""
        return self._current
    
    @current.setter
    def current(self, value: Union[int, None]):
        self._current = None if value is None else int(value)
        
    @property
    def frequency(self) -> Union[int, None]:
        """Frequency (in Hz)"""
        return self._frequency
    
    @frequency.setter
    def frequency(self, value: Union[int, None]):
        self._frequency = None if value is None else int(value)

    @property
    def idle_pwm(self) -> Union[float, None]:
        """Idle PWM value (0..1)"""
        return self._idle_pwm

    @idle_pwm.setter
    def idle_pwm(self, value: Union[float, None]):
        self._idle_pwm = None if value is None else float(value)
        
    @property
    def max(self) -> Union[int, None]:
        """Maximum RPM"""
        return self._max
    
    @max.setter
    def max(self, value: Union[int, None]):
        self._max = None if value is None else int(value)

    @property
    def max_pwm(self) -> Union[float, None]:
        """Maximum PWM value when turned on (0..1)"""
        return self._max_pwm

    @max_pwm.setter
    def max_pwm(self, value: Union[float, None]):
        self._max_pwm = None if value is None else float(value)
        
    @property
    def min(self) -> Union[int, None]:
        """Minimum RPM when turned on"""
        return self._min
    
    @min.setter
    def min(self, value: Union[int, None]):
        self._min = None if value is None else int(value)

    @property
    def min_pwm(self) -> Union[float, None]:
        """Minimum PWM value when turned on (0..1)"""
        return self._min_pwm

    @min_pwm.setter
    def min_pwm(self, value: Union[float, None]):
        self._min_pwm = None if value is None else float(value)
        
    @property
    def state(self) -> SpindleState:
        """Current state"""
        return self._state
    
    @state.setter
    def state(self, value):
        if value is None or value == "":
            self._state = SpindleState.unconfigured
        elif isinstance(value, str):
            self._state = SpindleState(value)
        elif isinstance(value, SpindleState):
            self._state = value
        else:
            raise TypeError(f"{__name__}.state must be of type SpindleState. Got {type(value)}: {value}")

    @property
    def type(self) -> SpindleType:
        """Spindle type"""
        return self._type

    @type.setter
    def type(self, value):
        if value is None or value == "":
            self._type = SpindleType.null
        elif isinstance(value, str):
            self._type = SpindleType(value)
        elif isinstance(value, SpindleType):
            self._type = value
        else:
            raise TypeError(f"{__name__}.type must be of type SpindleType. Got {type(value)}: {value}")
