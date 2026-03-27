from typing import List

from .tool_state import ToolState
from .tool_retraction import ToolRetraction
from ..model_object import ModelObject
from ..model_collection import ModelCollection
from ..utils import model_prop, nullable_model_prop
from ...utils import deprecated


class Tool(ModelObject):
    """Information about a configured tool"""

    active = model_prop('active', ModelCollection[float], ModelCollection(float))
    axes = model_prop('axes', ModelCollection[list[int]], ModelCollection(list[int]))
    extruders = model_prop('extruders', ModelCollection[int], ModelCollection(int))
    fans = model_prop('fans', ModelCollection[int], ModelCollection(int))
    feed_forward_advance = nullable_model_prop('feed_forward_advance', float)
    feed_forward_pwm = model_prop('feed_forward_pwm', ModelCollection[float], ModelCollection(float))
    feed_forward_temp = model_prop('feed_forward_temp', ModelCollection[float], ModelCollection(float))
    filament_extruder = model_prop('filament_extruder', int, -1)
    heaters = model_prop('heaters', ModelCollection[int], ModelCollection(int))
    is_retracted = model_prop('is_retracted', bool, False)
    mix = model_prop('mix', ModelCollection[float], ModelCollection(float))
    name = model_prop('name', str, "")
    number = model_prop('number', int, 0)
    offsets = model_prop('offsets', ModelCollection[float], ModelCollection(float))
    offsets_probed = model_prop('offsets_probed', int, 0)
    retraction = model_prop('retraction', ToolRetraction)
    spindle = model_prop('spindle', int, -1)
    spindle_rpm = model_prop('spindle_rpm', int, 0)
    standby = model_prop('standby', ModelCollection[float], ModelCollection(float))
    state = model_prop('state', ToolState, ToolState.off)

    def __init__(self):
        super().__init__()
