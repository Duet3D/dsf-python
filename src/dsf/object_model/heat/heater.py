from enum import Enum
from typing import List, Union

from .heater_model import HeaterModel
from .heater_monitor import HeaterMonitor
from ..model_collection import ModelCollection
from ..model_object import ModelObject


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
    def __init__(self):
        super().__init__()
        # Active temperature of the heater (in C)
        self._active = 0
        # Average heater PWM value (0..1)
        self._avg_pwm = 0
        # Current temperature of the heater (in C)
        self._current = -273.15
        # Current feedforward PWM boost applied to the heater
        self._extr_pwm_boost = None
        # Current temperature boost applied to the heater
        self._extr_temp_boost = None
        # Maximum temperature allowed for this heater (in C)
        # This is only temporary and should be replaced by a representation of the heater protection as in RRF
        self._max = 285
        # Maximum number of consecutive temperature reading failures before a heater fault is raised
        self._max_bad_readings = 3
        # Time for which a temperature anomaly must persist on this heater before raising a heater fault (in s)
        self._max_heating_fault_time = 5
        # Permitted temperature excursion from the setpoint for this heater (in K)
        self._max_temp_excursion = 15
        # Minimum temperature allowed for this heater (in C)
        # This is only temporary and should be replaced by a representation of the heater protection as in RRF
        self._min = -10
        # Information about the heater model
        self._model = HeaterModel()
        # Monitors of this heater
        self._monitors = ModelCollection(HeaterMonitor)
        # Sensor number of this heater or -1 if not configured
        self._sensor = -1
        # Standby temperature of the heater (in C)
        self._standby = 0
        # State of the heater
        self._state = HeaterState.off

    @property
    def active(self) -> float:
        """Active temperature of the heater (in C)"""
        return self._active

    @active.setter
    def active(self, value: float):
        self._active = float(value)

    @property
    def avg_pwm(self) -> float:
        """Average heater PWM value (0..1)"""
        return self._avg_pwm

    @avg_pwm.setter
    def avg_pwm(self, value: float):
        self._avg_pwm = float(value)

    @property
    def current(self) -> float:
        """Current temperature of the heater (in C)"""
        return self._current

    @current.setter
    def current(self, value: float):
        self._current = float(value)

    @property
    def extr_pwm_boost(self) -> Union[float, None]:
        """Current feedforward PWM boost applied to the heater"""
        return self._extr_pwm_boost

    @extr_pwm_boost.setter
    def extr_pwm_boost(self, value: Union[float, None]):
        self._extr_pwm_boost = float(value) if value is not None else None

    @property
    def extr_temp_boost(self) -> Union[float, None]:
        """Current temperature boost applied to the heater"""
        return self._extr_temp_boost

    @extr_temp_boost.setter
    def extr_temp_boost(self, value: Union[float, None]):
        self._extr_temp_boost = float(value) if value is not None else None

    @property
    def max(self) -> float:
        """Maximum temperature allowed for this heater (in C)
        This is only temporary and should be replaced by a representation of the heater protection as in RRF"""
        return self._max

    @max.setter
    def max(self, value: float):
        self._max = float(value)

    @property
    def max_bad_readings(self) -> int:
        """Maximum number of consecutive temperature reading failures before a heater fault is raised"""
        return self._max_bad_readings

    @max_bad_readings.setter
    def max_bad_readings(self, value: int):
        self._max_bad_readings = int(value)

    @property
    def max_heating_fault_time(self) -> float:
        """Time for which a temperature anomaly must persist on this heater before raising a heater fault (in s)"""
        return self._max_heating_fault_time

    @max_heating_fault_time.setter
    def max_heating_fault_time(self, value: float):
        self._max_heating_fault_time = float(value)

    @property
    def max_temp_excursion(self) -> float:
        """Permitted temperature excursion from the setpoint for this heater (in K)"""
        return self._max_temp_excursion

    @max_temp_excursion.setter
    def max_temp_excursion(self, value: float):
        self._max_temp_excursion = float(value)

    @property
    def min(self) -> float:
        """Minimum temperature allowed for this heater (in C)
        This is only temporary and should be replaced by a representation of the heater protection as in RRF"""
        return self._min

    @min.setter
    def min(self, value: float):
        self._min = float(value)

    @property
    def model(self) -> HeaterModel:
        """Information about the heater model"""
        return self._model

    @property
    def monitors(self) -> List[HeaterMonitor]:
        """Monitors of this heater"""
        return self._monitors

    @property
    def sensor(self) -> int:
        """Sensor number of this heater or -1 if not configured"""
        return self._sensor

    @sensor.setter
    def sensor(self, value: int):
        self._sensor = int(value)

    @property
    def standby(self) -> float:
        """Standby temperature of the heater (in C)"""
        return self._standby

    @standby.setter
    def standby(self, value: float):
        self._standby = float(value)

    @property
    def state(self) -> HeaterState:
        """State of the heater"""
        return self._state

    @state.setter
    def state(self, value: HeaterState):
        if isinstance(value, HeaterState):
            self._state = value
        elif isinstance(value, str):
            self._state = HeaterState(value)
        else:
            raise TypeError(f"{__name__}.state must be of type HeaterState. Got {type(value)}: {value}")
