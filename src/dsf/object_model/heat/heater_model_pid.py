from ..model_object import ModelObject
from ..utils import model_prop


class HeaterModelPID(ModelObject):
    """Details about the PID model of a heater"""

    # Derivative value of the PID regulator
    d = model_prop("d", float, 0)

    # Integral value of the PID regulator
    i = model_prop("i", float, 0)

    # Proportional value of the PID regulator
    p = model_prop("p", float, 0)

    # Indicates if PID control is being used
    used = model_prop("used", bool, True)

    def __init__(self):
        super().__init__()
