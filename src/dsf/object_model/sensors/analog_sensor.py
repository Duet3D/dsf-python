from typing import Union

from .analog_sensor_type import AnalogSensorType
from .temperature_error import TemperatureError
from ..model_object import ModelObject


class AnalogSensor(ModelObject):
    """Representation of an analog sensor"""

    def __init__(self):
        super(AnalogSensor, self).__init__()
        self._beta = None
        self._c = None
        self._high_reading = None
        self._last_reading = None
        self._low_reading = None
        self._name = None
        self._offset_adj = 0.0
        self._port = None
        self._r_25 = None
        self._r_ref = None
        self._slope_adj = 0.0
        self._state = TemperatureError.ok
        self._type = AnalogSensorType.Unknown

    @property
    def beta(self) -> Union[float, None]:
        """Beta value of this sensor (if applicable)"""
        return self._beta

    @beta.setter
    def beta(self, value):
        self._beta = float(value) if value is not None else None

    @property
    def c(self) -> Union[float, None]:
        """C value of this sensor"""
        return self._c

    @c.setter
    def c(self, value):
        self._c = float(value) if value is not None else None

    @property
    def high_reading(self) -> Union[float, None]:
        """High sensor reading (only linear analog sensors, otherwise null)"""
        return self._high_reading

    @high_reading.setter
    def high_reading(self, value):
        self._high_reading = float(value) if value is not None else None

    @property
    def last_reading(self) -> Union[float, None]:
        """Last sensor reading (in C) or null if invalid"""
        return self._last_reading
    
    @last_reading.setter
    def last_reading(self, value):
        self._last_reading = float(value) if value is not None else None

    @property
    def low_reading(self) -> Union[float, None]:
        """Low sensor reading (only linear analog sensors, otherwise null)"""
        return self._low_reading

    @low_reading.setter
    def low_reading(self, value):
        self._low_reading = float(value) if value is not None else None
        
    @property
    def name(self) -> Union[str, None]:
        """Name of this sensor or null if not configured"""
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = str(value) if value is not None else None
        
    @property
    def offset_adj(self) -> float:
        """Offset adjustment (in K)
        See also M308 U"""
        return self._offset_adj
    
    @offset_adj.setter
    def offset_adj(self, value):
        self._offset_adj = float(value)

    @property
    def port(self) -> Union[str, None]:
        """Port of this sensor or None if not applicable"""
        return self._port

    @port.setter
    def port(self, value):
        self._port = str(value) if value is not None else None

    @property
    def r_25(self) -> Union[float, None]:
        """Resistance of this sensor at 25C"""
        return self._r_25

    @r_25.setter
    def r_25(self, value):
        self._r_25 = float(value) if value is not None else None

    @property
    def r_ref(self) -> float:
        """Series resistance of this sensor channel"""
        return self._r_ref

    @r_ref.setter
    def r_ref(self, value):
        self._r_ref = float(value) if value is not None else None

    @property
    def slope_adj(self) -> float:
        """Slope adjustment factor
        See also M308 V"""
        return self._slope_adj

    @slope_adj.setter
    def slope_adj(self, value):
        self._slope_adj = float(value)

    @property
    def state(self) -> TemperatureError:
        """State of this sensor"""
        return self._state

    @state.setter
    def state(self, value):
        if isinstance(value, TemperatureError):
            self._state = value
        else:
            self._state = TemperatureError(value)
        
    @property
    def type(self) -> AnalogSensorType:
        """Type of this sensor"""
        return self._type
    
    @type.setter
    def type(self, value):
        if value is None:
            self._type = AnalogSensorType.Unknown
        elif isinstance(value, AnalogSensorType):
            self._type = value
        elif isinstance(value, str):
            self._type = AnalogSensorType(value)
        else:
            raise TypeError(f"{__name__}.type must be of type AnalogSensorType or None. Got {type(value)}: {value}")
