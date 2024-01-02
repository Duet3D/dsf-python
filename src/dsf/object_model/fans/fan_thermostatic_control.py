from typing import List, Union
from ..model_object import ModelObject
from ...utils import deprecated


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
    @deprecated(f"Use {__name__}.sensors instead")
    def heaters(self) -> List[int]:
        """List of the heaters to monitor (indices)
        Deprecated: Use sensors instead"""
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
