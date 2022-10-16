from enum import Enum
from typing import List

from .heater_model import HeaterModel
from .heater_monitor import HeaterMonitor
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
        # Maximum temperature allowed for this heater (in C)
        # This is only temporary and should be replaced by a representation of the heater protection as in RRF
        self._max = 285
        # Minimum temperature allowed for this heater (in C)
        # This is only temporary and should be replaced by a representation of the heater protection as in RRF
        self._min = -10
        # Information about the heater model
        self._model = HeaterModel()
        # Monitors of this heater
        self._monitors = []
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
        self._active = float(value) if value is not None else 0

    @property
    def avg_pwm(self) -> float:
        """Average heater PWM value (0..1)"""
        return self._avg_pwm

    @avg_pwm.setter
    def avg_pwm(self, value: float):
        self._avg_pwm = float(value) if value is not None else 0

    @property
    def current(self) -> float:
        """Current temperature of the heater (in C)"""
        return self._current

    @current.setter
    def current(self, value: float):
        self._current = float(value) if value is not None else -273.15

    @property
    def max(self) -> float:
        """Maximum temperature allowed for this heater (in C)
        This is only temporary and should be replaced by a representation of the heater protection as in RRF"""
        return self._max

    @max.setter
    def max(self, value: float):
        self._max = float(value) if value is not None else 285

    @property
    def min(self) -> float:
        """Minimum temperature allowed for this heater (in C)
        This is only temporary and should be replaced by a representation of the heater protection as in RRF"""
        return self._min

    @min.setter
    def min(self, value: float):
        self._min = float(value) if value is not None else -10

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
        self._sensor = int(value) if value is not None else -1

    @property
    def standby(self) -> float:
        """Standby temperature of the heater (in C)"""
        return self._standby

    @standby.setter
    def standby(self, value: float):
        self._standby = float(value) if value is not None else 0

    @property
    def state(self) -> HeaterState:
        """State of the heater"""
        return self._state

    @state.setter
    def state(self, value: HeaterState):
        self._state = value

    def _update_from_json(self, **kwargs) -> 'Heater':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(Heater, self)._update_from_json(**kwargs)
        self._model = HeaterModel.from_json(kwargs.get('model'))
        self._monitors = [HeaterMonitor.from_json(monitor) for monitor in kwargs.get('monitors', [])]
        return self
