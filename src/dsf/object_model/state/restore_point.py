from typing import List, Union


from ..model_object import ModelObject
from ..model_collection import ModelCollection
from ..utils import model_prop, nullable_model_prop


class RestorePoint(ModelObject):
    """
    Class holding information about a restore point
    """

    coords = model_prop('coords', ModelCollection[float], ModelCollection(float))
    extruder_pos = model_prop('extruder_pos', float, 0)
    fan_pwm = model_prop('fan_pwm', float, 0)
    feed_rate = model_prop('feed_rate', float, 0)
    io_bits = nullable_model_prop('io_bits', int)
    laser_pwm = nullable_model_prop('laser_pwm', float)
    tool_number = model_prop('tool_number', int, -1)

    def __init__(self):
        super(RestorePoint, self).__init__()
