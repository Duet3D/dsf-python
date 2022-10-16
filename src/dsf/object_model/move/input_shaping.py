from enum import Enum
from typing import List

from ..model_object import ModelObject


class InputShapingType(str, Enum):
    """Enumeration of possible input shaping methods"""

    # none
    none = "none"

    # MZV
    mzv = "mzv"

    # ZVD
    zvd = "zvd"

    # ZVDD
    zvdd = "zvdd"

    # ZVDDD
    zvddd = "zvddd"

    # EI2 (2-hump)
    ei2 = "ei2"

    # EI3 (3-hump)
    ei3 = "ei3"

    # Custom
    custom = "custom"


class InputShaping(ModelObject):
    """Parameters describing input shaping """
    def __init__(self):
        super().__init__()
        # Amplitudes of the input shaper
        self._amplitudes = []
        # Damping factor
        self._damping = 0.1
        # Input shaper durations (in s)
        self._durations = []
        # Frequency (in Hz)
        self._frequency = 40
        # Minimum acceleration (in mm/s)
        self._min_acceleration = 10
        # Configured input shaping type
        self._type = InputShapingType.none

    @property
    def amplitudes(self) -> List[float]:
        """Amplitudes of the input shaper"""
        return self._amplitudes

    @property
    def damping(self) -> float:
        """Damping factor"""
        return self._damping

    @damping.setter
    def damping(self, value):
        self._damping = float(value) if value is not None else 0.1

    @property
    def durations(self) -> List[float]:
        """Input shaper durations (in s)"""
        return self._durations

    @property
    def frequency(self) -> float:
        """Frequency (in Hz)"""
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = float(value) if value is not None else 40

    @property
    def min_acceleration(self) -> float:
        """Minimum acceleration (in mm/s)"""
        return self._min_acceleration

    @min_acceleration.setter
    def min_acceleration(self, value):
        self._min_acceleration = float(value) if value is not None else 10

    @property
    def type(self) -> InputShapingType:
        """Configured input shaping type"""
        return self._type

    @type.setter
    def type(self, value):
        if isinstance(value, InputShapingType):
            self._type = value
        elif isinstance(value, str):
            self._type = InputShapingType(value)
        else:
            raise TypeError(f"{__name__}.type must be of type InputShapingType. Got {type(value)}: {value}")

    def _update_from_json(self, **kwargs) -> 'InputShaping':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(InputShaping, self)._update_from_json(**kwargs)
        self._amplitudes = [float(a) for a in kwargs.get('amplitudes', [])]
        self._durations = [float(d) for d in kwargs.get('durations', [])]
        return self
