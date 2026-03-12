from ..model_object import ModelObject


class MicroStepping(ModelObject):
    """Microstepping configuration"""

    def __init__(self) -> None:
        super().__init__()
        # Indicates if the stepper driver uses interpolation
        self._interpolated: bool = False
        # Microsteps per full step
        self._value: int = 16

    @property
    def interpolated(self) -> bool:
        """"Indicates if the stepper driver uses interpolation"""
        return self._interpolated

    @interpolated.setter
    def interpolated(self, value: bool | int | str):
        self._interpolated = bool(value)

    @property
    def value(self) -> int:
        """Microsteps per full step"""
        return self._value

    @value.setter
    def value(self, value: int | str):
        self._value = int(value)
