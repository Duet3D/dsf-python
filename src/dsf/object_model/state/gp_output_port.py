from ..model_object import ModelObject
from ..utils import model_prop


class GpOutputPort(ModelObject):
    """Details about a general-purpose output port"""

    # PWM frequency of this port (in Hz)
    freq = model_prop("freq", int, 0)

    # PWM value of this port (0..1)
    pwm = model_prop("pwm", float, 0)

    def __init__(self):
        super(GpOutputPort, self).__init__()
