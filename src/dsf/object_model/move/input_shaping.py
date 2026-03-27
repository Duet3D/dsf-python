from enum import Enum
from typing import List


from ..model_object import ModelObject
from ..model_collection import ModelCollection
from ..utils import model_prop


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

    # Amplitudes of the input shaper
    amplitudes = model_prop("amplitudes", ModelCollection[float], ModelCollection(float))

    # Damping factor
    damping = model_prop("damping", float, 0.1)

    # Input shaper delays (in s)
    delays = model_prop("delays", ModelCollection[float], ModelCollection(float))

    # Input shaper durations (in s)
    durations = model_prop("durations", ModelCollection[float], ModelCollection(float))

    # Frequency (in Hz)
    frequency = model_prop("frequency", float, 40.0)

    # Minimum fraction of the original acceleration or feed rate to which the acceleration or feed rate may be reduced in order to apply input shaping
    reduction_limit = model_prop("reduction_limit", float, 0.25)

    # Configured input shaping type
    type = model_prop("type", InputShapingType, InputShapingType.none)

    def __init__(self):
        super().__init__()