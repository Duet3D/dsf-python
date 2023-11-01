from ..model_object import ModelObject


class GpInputPort(ModelObject):
    """Details about a general-purpose input port"""

    def __init__(self):
        super(GpInputPort, self).__init__()
        self._value = 0

    @property
    def value(self) -> float:
        """Value of this port (0..1)"""
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = float(value)
