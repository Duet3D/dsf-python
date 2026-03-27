from .move_deviations import MoveDeviations
from ..model_object import ModelObject
from ..utils import model_prop


class MoveCalibration(ModelObject):
    """Information about configured calibration options"""

    # Final calibration results (for Delta calibration)
    final = model_prop("final", MoveDeviations)

    # Initial calibration results (for Delta calibration)
    initial = model_prop("initial", MoveDeviations)

    # Number of factors used (for Delta calibration)
    num_factors = model_prop("num_factors", int, 0)

    def __init__(self):
        super().__init__()
