from ..model_object import ModelObject


class MoveDeviations(ModelObject):
    """Calibration or mesh grid results"""

    def __init__(self) -> None:
        super().__init__()
        # RMS deviation (in mm)
        self._deviation: float = 0
        # Mean deviation (in mm)
        self._mean: float = 0

    @property
    def deviation(self) -> float:
        """RMS deviation (in mm)"""
        return self._deviation

    @deviation.setter
    def deviation(self, value: float | int | str):
        self._deviation = float(value)

    @property
    def mean(self) -> float:
        """Mean deviation (in mm)"""
        return self._mean

    @mean.setter
    def mean(self, value: float | int | str):
        self._mean = float(value)
