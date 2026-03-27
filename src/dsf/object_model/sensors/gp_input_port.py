from ..model_object import ModelObject
from ..utils import model_prop


class GpInputPort(ModelObject):
    """Details about a general-purpose input port"""

    # Value of this port (0..1)
    value = model_prop("value", float, 0)

    def __init__(self):
        super(GpInputPort, self).__init__()
