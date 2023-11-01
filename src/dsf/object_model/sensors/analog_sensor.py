from __future__ import annotations

from .analog_sensor_type import AnalogSensorType
from ..model_object import ModelObject


class AnalogSensor(ModelObject):
    """Representation of an analog sensor"""

    def __init__(self):
        super(AnalogSensor, self).__init__()
        self._last_reading = None
        self._name = None
        self._type = AnalogSensorType.Unknown

    @property
    def last_reading(self) -> float | None:
        """Last sensor reading (in C) or null if invalid"""
        return self._last_reading
    
    @last_reading.setter
    def last_reading(self, value: float | None = None):
        self._last_reading = float(value) if value is not None else None
        
    @property
    def name(self) -> str | None:
        """Name of this sensor or null if not configured"""
        return self._name
    
    @name.setter
    def name(self, value: str | None = None):
        self._name = str(value) if value is not None else None
        
    @property
    def type(self) -> AnalogSensorType:
        """Type of this sensor"""
        return self._type
    
    @type.setter
    def type(self, value: AnalogSensorType = AnalogSensorType.Unknown):
        if isinstance(value, AnalogSensorType):
            self._type = value
        elif isinstance(value, str):
            self._type = AnalogSensorType(value)
        else:
            raise TypeError(f"{__name__}.type must be of type AnalogSensorType."
                            f" Got {type(value)}: {value}")
