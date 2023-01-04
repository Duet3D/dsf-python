from __future__ import annotations
from ..model_object import ModelObject


class FanThermostaticControl(ModelObject):
    """Thermostatic parameters of a fan"""
    def __init__(self):
        super().__init__()
        # List of the heaters to monitor (indices)
        self._heaters = []
        # Upper temperature range required to turn on the fan (in C)
        self._high_temperature = None
        # Lower temperature range required to turn on the fan (in C)
        self._low_temperature = None

    @property
    def heaters(self) -> list[int]:
        """List of the heaters to monitor (indices)"""
        return self._heaters

    @property
    def high_temperature(self) -> float | None:
        """Upper temperature range required to turn on the fan (in C)"""
        return self._high_temperature

    @high_temperature.setter
    def high_temperature(self, value: float | None = None):
        self._high_temperature = float(value) if value is not None else None

    @property
    def low_temperature(self) -> float | None:
        """Lower temperature range required to turn on the fan (in C)"""
        return self._low_temperature

    @low_temperature.setter
    def low_temperature(self, value: float | None = None):
        self._low_temperature = float(value) if value is not None else None
