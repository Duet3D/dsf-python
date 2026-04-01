from typing import List, Optional

from .model_collection import ModelCollection
from .model_dictionary import ModelDictionary
from .model_object import ModelObject
from .boards import Board
from .directories import Directories
from .fans import Fan
from .heat import Heat
from .inputs import Inputs
from .job import Job
from .led_strips import LedStrip
from .limits import Limits
from .messages import Message
from .move import Move
from .network import Network
from .plugins import Plugin
from .sbc import SBC
from .sensors import Sensors
from .spindles import Spindle
from .state import State
from .tools import Tool
from .volumes import Volume

from .utils import nullable_model_prop, model_prop


class ObjectModel(ModelObject):

    # Information about the SBC which Duet Software Framework is running on.
    # This is None if the system is operating in standalone mode
    boards = model_prop('boards', ModelCollection[Board], ModelCollection(Board))
    directories = model_prop('directories', Directories)
    fans = model_prop('fans', ModelCollection[Optional[Fan]], ModelCollection(Optional[Fan]))
    globals = model_prop('globals', ModelDictionary, ModelDictionary(False))
    heat = model_prop('heat', Heat)
    inputs = model_prop('inputs', Inputs)
    job = model_prop('job', Job)
    led_strips = model_prop('led_strips', ModelCollection[LedStrip], ModelCollection(LedStrip))
    limits = model_prop('limits', Limits)
    messages = model_prop('messages', ModelCollection[Message], ModelCollection(Message))
    move = model_prop('move', Move)
    network = model_prop('network', Network)
    plugins = model_prop('plugins', ModelDictionary, ModelDictionary(True, Plugin))
    sbc = nullable_model_prop('sbc', SBC)
    sensors = model_prop('sensors', Sensors)
    spindles = model_prop('spindles', ModelCollection[Optional[Spindle]], ModelCollection(Optional[Spindle]))
    state = model_prop('state', State)
    tools = model_prop('tools', ModelCollection[Optional[Tool]], ModelCollection(Optional[Tool]))
    volumes = model_prop('volumes', ModelCollection[Volume], ModelCollection(Volume))


    def __init__(self):
        super(ObjectModel, self).__init__()

    def _update_from_json(self, **kwargs) -> 'ObjectModel':
        super(ObjectModel, self)._update_from_json(**kwargs)

        # "global" is a reserved keyword in Python, so it is converted to "globals"
        if 'global_' in kwargs:
            self.globals.update_from_json(kwargs.get('global_'))
        return self
