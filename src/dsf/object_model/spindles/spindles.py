from .spindle_state import SpindleState
from ..model_object import ModelObject


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
        # Maximum RPM
        self._max = 10000
        # Minimum RPM when turned on
        self._min = 60
        # Current state
        self._state = SpindleState.unconfigured
        
    @property
    def active(self) -> int:
        """Active RPM"""
        return self._active
    
    @active.setter
    def active(self, value: int):
        self._active = int(value)
        
    @property
    def can_reverse(self) -> bool:
        """Flags whether the spindles may spin in reverse direction"""
        return self._can_reverse
    
    @can_reverse.setter
    def can_reverse(self, value: bool):
        self._can_reverse = bool(value)
        
    @property
    def current(self) -> int:
        """Current RPM, negative if anticlockwise direction"""
        return self._current
    
    @current.setter
    def current(self, value: int):
        self._current = int(value)
        
    @property
    def frequency(self) -> int:
        """Frequency (in Hz)"""
        return self._frequency
    
    @frequency.setter
    def frequency(self, value: int):
        self._frequency = int(value)
        
    @property
    def max(self) -> int:
        """Maximum RPM"""
        return self._max
    
    @max.setter
    def max(self, value: int):
        self._max = int(value)
        
    @property
    def min(self) -> int:
        """Minimum RPM when turned on"""
        return self._min
    
    @min.setter
    def min(self, value: int):
        self._min = int(value)
        
    @property
    def state(self) -> SpindleState:
        """Current state"""
        return self._state
    
    @state.setter
    def state(self, value: SpindleState = SpindleState.unconfigured):
        if isinstance(value, SpindleState):
            self._state = value
        elif isinstance(value, str):
            self._state = SpindleState(value)
        else:
            raise TypeError(f"{__name__}.state must be of type SpindleState."
                            f" Got {type(value)}: {value}")
