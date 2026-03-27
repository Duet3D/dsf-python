from ..model_object import ModelObject
from ..utils import model_prop


class MoveDeviations(ModelObject):
    """Calibration or mesh grid results"""

    # RMS deviation (in mm)
    deviation = model_prop("deviation", float, 0)

    # Mean deviation (in mm)
    mean = model_prop("mean", float, 0)

    def __init__(self):
        super().__init__()
