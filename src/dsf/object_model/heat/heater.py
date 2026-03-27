from enum import Enum

from .heater_model import HeaterModel
from .heater_monitor import HeaterMonitor
from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import model_prop, nullable_model_prop


class HeaterState(str, Enum):
    """State of a heater"""

    # Heater is turned off
    off = "off"

    # Heater is in standby mode
    standby = "standby"

    # Heater is active
    active = "active"

    # Heater faulted
    fault = "fault"

    # Heater is being tuned
    tuning = "tuning"

    # Heater is offline
    offline = "offline"


class Heater(ModelObject):
    """Information about a heater"""

    # Active temperature of the heater (in C)
    active = model_prop("active", float, 0)

    # Average heater PWM value (0..1)
    avg_pwm = model_prop("avg_pwm", float, 0)

    # Current temperature of the heater (in C)
    current = model_prop("current", float, -273.15)

    # Current feedforward PWM boost applied to the heater
    extr_pwm_boost = nullable_model_prop("extr_pwm_boost", float)

    # Current temperature boost applied to the heater
    extr_temp_boost = nullable_model_prop("extr_temp_boost", float)

    # Maximum temperature allowed for this heater (in C)
    max = model_prop("max", float, 285)

    # Maximum number of consecutive temperature reading failures before a heater fault is raised
    max_bad_readings = model_prop("max_bad_readings", int, 3)

    # Time for which a temperature anomaly must persist on this heater before raising a heater fault (in s)
    max_heating_fault_time = model_prop("max_heating_fault_time", float, 5)

    # Permitted temperature excursion from the setpoint for this heater (in K)
    max_temp_excursion = model_prop("max_temp_excursion", float, 15)

    # Minimum temperature allowed for this heater (in C)
    min = model_prop("min", float, -10)

    # Information about the heater model
    model = model_prop("model", HeaterModel, HeaterModel())

    # Monitors of this heater
    monitors = model_prop("monitors", ModelCollection[HeaterMonitor], ModelCollection(HeaterMonitor))

    # Sensor number of this heater or -1 if not configured
    sensor = model_prop("sensor", int, -1)

    # Standby temperature of the heater (in C)
    standby = model_prop("standby", float, 0)

    # State of the heater
    state = model_prop("state", HeaterState, HeaterState.off)

    def __init__(self):
        super().__init__()
