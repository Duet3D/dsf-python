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
    ei2 = "eI2"

    # EI3 (3-hump)
    ei3 = "eI3"

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
        # Input shaper delays (in s)
        self._delays = []
        # Frequency (in Hz)
        self._frequency = 40
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
        self._damping = float(value)

    @property
    def delays(self) -> List[float]:
        """Input shaper delays (in s)"""
        return self._delays

    @property
    def frequency(self) -> float:
        """Frequency (in Hz)"""
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = float(value)

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
