from ..model_object import ModelObject
from ..utils import model_prop


class MicroStepping(ModelObject):
    """Microstepping configuration"""

    # Indicates if the stepper driver uses interpolation
    interpolated = model_prop("interpolated", bool, False)

    # Microsteps per full step
    value = model_prop("value", int, 16)

    def __init__(self):
        super().__init__()
