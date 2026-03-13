from ..model_object import ModelObject
from .heater_model_pid import HeaterModelPID
from ..utils import model_prop


class HeaterModel(ModelObject):
    """Information about the way the heater heats up"""

    # Cooling rate exponent
    cooling_exp = model_prop("cooling_exp", float, 1.35)

    # Cooling rate (in K/s)
    cooling_rate = model_prop("cooling_rate", float, 0.56)

    # Dead time (in s)
    dead_time = model_prop("dead_time", float, 5.5)

    # Indicates if this heater is enabled
    enabled = model_prop("enabled", bool, False)

    # Cooling rate with the fan on (in K/s)
    fan_cooling_rate = model_prop("fan_cooling_rate", float, 0.56)

    # Heating rate (in K/s)
    heating_rate = model_prop("heating_rate", float, 2.43)

    # Indicates if the heater PWM signal is inverted
    inverted = model_prop("inverted", bool, False)

    # Maximum PWM value
    max_pwm = model_prop("max_pwm", float, 1)

    # Details about the PID controller
    pid = model_prop("pid", HeaterModelPID)

    # Standard voltage
    standard_voltage = model_prop("standard_voltage", float)

    def __init__(self):
        super().__init__()
