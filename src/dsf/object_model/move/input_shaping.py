from enum import Enum


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
    ei2 = "ei2"

    # EI3 (3-hump)
    ei3 = "ei3"

    # Custom
    custom = "custom"

    @classmethod
    def _missing_(cls, value: object):
        # DSF versions prior to 3.7 serialized EI2/EI3 as "eI2"/"eI3"
        if isinstance(value, str):
            for member in cls:
                if member.value == value.lower():
                    return member
        return None


class InputShaping(ModelObject):
    """Parameters describing input shaping"""

    # Amplitudes of the input shaper
    amplitudes = model_prop("amplitudes", ModelCollection[float], ModelCollection(float))

    # Damping factor
    damping = model_prop("damping", float, 0.1)

    # Input shaper delays (in s)
    delays = model_prop("delays", ModelCollection[float], ModelCollection(float))

    # Frequency (in Hz)
    frequency = model_prop("frequency", float, 40.0)

    # Configured input shaping type
    type = model_prop("type", InputShapingType, InputShapingType.none)

    def __init__(self):
        super().__init__()
