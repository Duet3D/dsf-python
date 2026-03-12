from ..model_object import ModelObject


class GpOutputPort(ModelObject):
    """Details about a general-purpose output port"""

    def __init__(self) -> None:
        super(GpOutputPort, self).__init__()
        # PWM frequency of this port (in Hz)
        self._freq: int = 0
        # PWM value of this port (0..1)
        self._pwm: float = 0

    @property
    def freq(self) -> int:
        """PWM frequency of this port (in Hz)"""
        return self._freq

    @freq.setter
    def freq(self, value: int | str):
        self._freq = int(value)

    @property
    def pwm(self) -> float:
        """PWM value of this port (0..1)"""
        return self._pwm

    @pwm.setter
    def pwm(self, value: float | int | str):
        self._pwm = float(value)
