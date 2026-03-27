from typing import Union

from .analog_sensor_type import AnalogSensorType
from .temperature_error import TemperatureError
from ..model_object import ModelObject
from ..utils import model_prop, nullable_model_prop


class AnalogSensor(ModelObject):
    """Representation of an analog sensor"""

    beta = nullable_model_prop('beta', float)
    c = nullable_model_prop('c', float)
    high_reading = nullable_model_prop('high_reading', float)
    last_reading = nullable_model_prop('last_reading', float)
    low_reading = nullable_model_prop('low_reading', float)
    name = nullable_model_prop('name', str)
    offset_adj = model_prop('offset_adj', float, 0.0)
    port = nullable_model_prop('port', str)
    r_25 = nullable_model_prop('r_25', float)
    r_ref = nullable_model_prop('r_ref', float)
    slope_adj = model_prop('slope_adj', float, 0.0)
    state = model_prop('state', TemperatureError, TemperatureError.ok)
    type = model_prop('type', AnalogSensorType, AnalogSensorType.Unknown)

    def __init__(self):
        super(AnalogSensor, self).__init__()
