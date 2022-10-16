from .move_deviations import MoveDeviations
from ..model_object import ModelObject


class MoveCalibration(ModelObject):
    """Information about configured calibration options"""
    def __init__(self):
        super().__init__()
        # Final calibration results (for Delta calibration)
        self._final = MoveDeviations()
        # Initial calibration results (for Delta calibration)
        self._initial = MoveDeviations()
        # Number of factors used (for Delta calibration)
        self._num_factors = 0

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
    def num_factors(self, value):
        self._num_factors = int(value) if value is not None else 0

    def _update_from_json(self, **kwargs) -> 'MoveCalibration':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(MoveCalibration, self)._update_from_json(**kwargs)
        self._final = MoveDeviations.from_json(kwargs.get('final'))
        self._initial = MoveDeviations.from_json(kwargs.get('initial'))
        return self
