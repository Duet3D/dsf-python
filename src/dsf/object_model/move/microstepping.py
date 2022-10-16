from ..model_object import ModelObject


class MicroStepping(ModelObject):
    """Microstepping configuration"""
    def __init__(self):
        super().__init__()
        # Indicates if the stepper driver uses interpolation
        self._interpolated = False
        # Microsteps per full step
        self._value = 16

    @property
    def interpolated(self) -> bool:
        """"Indicates if the stepper driver uses interpolation"""
        return self._interpolated

    @interpolated.setter
    def interpolated(self, value):
        self._interpolated = bool(value)

    @property
    def value(self) -> int:
        """Microsteps per full step"""
        return self._value

    @value.setter
    def value(self, value):
        self._value = int(value) if value is not None else 16
