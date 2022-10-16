from ..model_object import ModelObject


class GpOutputPort(ModelObject):
    """Details about a general-purpose output port"""

    def __init__(self):
        super(GpOutputPort, self).__init__()
        self._pwm = 0

    @property
    def pwm(self) -> float:
        """PWM value of this port (0..1)"""
        return self._pwm

    @pwm.setter
    def pwm(self, value):
        self._pwm = float(value) if value is not None else 0
