from __future__ import annotations

from ..model_object import ModelObject
from .heater_model_pid import HeaterModelPID


class HeaterModel(ModelObject):
    """Information about the way the heater heats up"""

    def __init__(self):
        super().__init__()
        # Cooling rate exponent
        self._cooling_exp = 1.35
        # Cooling rate (in K/s)
        self._cooling_rate = 0.56
        # Dead time (in s)
        self._dead_time = 5.5
        # Indicates if this heater is enabled
        self._enabled = False
        # Cooling rate with the fan on (in K/s)
        self._fan_cooling_rate = 0.56
        # Heating rate (in K/s)
        self._heating_rate = 2.43
        # Indicates if the heater PWM signal is inverted
        self._inverted = False
        # Maximum PWM value
        self._max_pwm = 1
        # Details about the PID controller
        self._pid = HeaterModelPID()
        # Standard voltage or None if unknown
        self._standard_voltage = None

    @property
    def cooling_exp(self) -> float:
        """Cooling rate exponent"""
        return self._cooling_exp

    @cooling_exp.setter
    def cooling_exp(self, value: float):
        self._cooling_exp = float(value)

    @property
    def cooling_rate(self) -> float:
        """Cooling rate (in K/s)"""
        return self._cooling_rate

    @cooling_rate.setter
    def cooling_rate(self, value: float):
        self._cooling_rate = float(value)

    @property
    def dead_time(self) -> float:
        """Dead time (in s)"""
        return self._dead_time

    @dead_time.setter
    def dead_time(self, value: float):
        self._dead_time = float(value)

    @property
    def enabled(self) -> bool:
        """Indicates if this heater is enabled"""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = bool(value)

    @property
    def fan_cooling_rate(self) -> float:
        """Cooling rate with the fan on (in K/s)"""
        return self._fan_cooling_rate

    @fan_cooling_rate.setter
    def fan_cooling_rate(self, value: float):
        self._fan_cooling_rate = float(value)

    @property
    def heating_rate(self) -> float:
        """Heating rate (in K/s)"""
        return self._heating_rate

    @heating_rate.setter
    def heating_rate(self, value: float):
        self._heating_rate = float(value)

    @property
    def inverted(self) -> bool:
        """Indicates if the heater PWM signal is inverted"""
        return self._inverted

    @inverted.setter
    def inverted(self, value: bool):
        self._inverted = bool(value)

    @property
    def max_pwm(self) -> float:
        """Maximum PWM value"""
        return self._max_pwm

    @max_pwm.setter
    def max_pwm(self, value: float):
        self._max_pwm = float(value)

    @property
    def pid(self) -> HeaterModelPID:
        """Details about the PID controller"""
        return self._pid

    @property
    def standard_voltage(self) -> float | None:
        """Standard voltage or null if unknown"""
        return self._standard_voltage

    @standard_voltage.setter
    def standard_voltage(self, value):
        self._standard_voltage = float(value) if value is not None else None
