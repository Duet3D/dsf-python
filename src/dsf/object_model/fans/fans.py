from .fan_thermostatic_control import FanThermostaticControl
from ..model_object import ModelObject
from ..utils import model_prop


class Fan(ModelObject):
    """Class representing information about an attached fan"""

    # Value of this fan (0..1 or -1 if unknown)
    actual_value = model_prop("actual_value", float)

    # Blip value indicating how long the fan is supposed to run at 100% when turning it on to get it started (in s)
    blip = model_prop("blip", float, 0.1)

    # Configured frequency of this fan (in Hz)
    frequency = model_prop("frequency", float, 250)

    # Maximum value of this fan (0..1)
    max = model_prop("max", float, 1)

    # Minimum value of this fan (0..1)
    min = model_prop("min", float)

    # Name of the fan
    name = model_prop("name", str)

    # Requested value for this fan on a scale between 0 and 1
    requested_value = model_prop("requested_value", float)

    # Current RPM of this fan or -1 if unknown/unset
    rpm = model_prop("rpm", int, -1)

    # Pulses per tacho revolution
    tacho_ppr = model_prop("tacho_ppr", float, 2.0)

    # Thermostatic control parameters
    thermostatic = model_prop("thermostatic", FanThermostaticControl)

    def __init__(self):
        super().__init__()
