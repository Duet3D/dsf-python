from typing import List, Union
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
        # List of sensors to monitor (indices)
        self._sensors = []

    @property
    def heaters(self) -> List[int]:
        # TODO: set deprecated flag
        """Deprecated as of v3.5, use sensors instead
        List of the heaters to monitor (indices)"""
        return self._heaters

    @property
    def high_temperature(self) -> Union[float, None]:
        """Upper temperature range required to turn on the fan (in C)"""
        return self._high_temperature

    @high_temperature.setter
    def high_temperature(self, value):
        self._high_temperature = float(value) if value is not None else None

    @property
    def low_temperature(self) -> Union[float, None]:
        """Lower temperature range required to turn on the fan (in C)"""
        return self._low_temperature

    @low_temperature.setter
    def low_temperature(self, value):
        self._low_temperature = float(value) if value is not None else None

    @property
    def sensors(self) -> List[int]:
        """List of sensors to monitor (indices)"""
        return self._sensors
