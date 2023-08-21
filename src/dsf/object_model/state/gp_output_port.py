from ..model_object import ModelObject


class GpOutputPort(ModelObject):
    """Details about a general-purpose output port"""

    def __init__(self):
        super(GpOutputPort, self).__init__()
        # PWM frequency of this port (in Hz)
        self._freq = 0
        # PWM value of this port (0..1)
        self._pwm = 0

    @property
    def freq(self) -> int:
        """PWM frequency of this port (in Hz)"""
        return self._freq

    @freq.setter
    def freq(self, value):
        self._freq = int(value)

    @property
    def pwm(self) -> float:
        """PWM value of this port (0..1)"""
        return self._pwm

    @pwm.setter
    def pwm(self, value):
        self._pwm = float(value)
