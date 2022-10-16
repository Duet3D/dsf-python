from typing import Union

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
    def last_reading(self) -> Union[float, None]:
        """Last sensor reading (in C) or null if invalid"""
        return self._last_reading
    
    @last_reading.setter
    def last_reading(self, value):
        self._last_reading = float(value) if value is not None else None
        
    @property
    def name(self) -> Union[str, None]:
        """Name of this sensor or null if not configured"""
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = str(value) if value is not None else None
        
    @property
    def type(self) -> AnalogSensorType:
        """Type of this sensor"""
        return self._type
    
    @type.setter
    def type(self, value):
        if value is None or isinstance(value, AnalogSensorType):
            self._type = value
        elif isinstance(value, str):
            self._type = AnalogSensorType(value)
        else:
            raise TypeError(f"{__name__}.type must be of type AnalogSensorType or None. Got {type(value)}: {value}")
