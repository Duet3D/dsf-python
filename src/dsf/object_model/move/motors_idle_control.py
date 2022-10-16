from ..model_object import ModelObject


class MotorsIdleControl(ModelObject):
    """Idle factor parameters for automatic motor current reduction"""
    def __init__(self):
        super().__init__()
        # Motor current reduction factor (0..1)
        self._factor = 0.3
        # Idle timeout after which the stepper motor currents are reduced (in s)
        self._timeout = 30

    @property
    def factor(self) -> float:
        """Motor current reduction factor (0..1)"""
        return self._factor

    @factor.setter
    def factor(self, value):
        self._factor = float(value) if value is not None else 0.3

    @property
    def timeout(self) -> float:
        """Idle timeout after which the stepper motor currents are reduced (in s)"""
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = float(value) if value is not None else 30
