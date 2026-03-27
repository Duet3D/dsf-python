from ..model_object import ModelObject
from ..utils import model_prop


class ProbeTouchMode(ModelObject):
    """Information about a configured probe"""

    active = model_prop("active", bool)
    speed = model_prop("speed", float)
    threshold = model_prop("threshold", float)
    trigger_height = model_prop("trigger_height", float)

    def __init__(self):
        super(ProbeTouchMode, self).__init__()