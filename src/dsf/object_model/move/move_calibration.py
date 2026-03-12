from .move_deviations import MoveDeviations
from ..model_object import ModelObject


class MoveCalibration(ModelObject):
    """Information about configured calibration options"""

    def __init__(self) -> None:
        super().__init__()
        # Final calibration results (for Delta calibration)
        self._final: MoveDeviations = MoveDeviations()
        # Initial calibration results (for Delta calibration)
        self._initial: MoveDeviations = MoveDeviations()
        # Number of factors used (for Delta calibration)
        self._num_factors: int = 0

    @property
    def final(self) -> MoveDeviations:
        """Final calibration results (for Delta calibration)"""
        return self._final

    @property
    def initial(self) -> MoveDeviations:
        """Initial calibration results (for Delta calibration)"""
        return self._initial

    @property
    def num_factors(self) -> int:
        """Number of factors used (for Delta calibration)"""
        return self._num_factors

    @num_factors.setter
    def num_factors(self, value: int | str):
        self._num_factors = int(value)
