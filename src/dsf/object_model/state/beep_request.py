from ..model_object import ModelObject
from ..utils import model_prop


class BeepRequest(ModelObject):
    """Details about a requested beep"""

    duration = model_prop("duration", int, 0)
    frequency = model_prop("frequency", int, 0)

    def __init__(self):
        super(BeepRequest, self).__init__()
