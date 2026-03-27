from ...model_object import ModelObject
from ...utils import model_prop


class DeltaTower(ModelObject):
    """Delta tower properties"""

    # Tower position corrections (in degrees)
    angle_correction = model_prop("angle_correction", float, 0)

    # Diagonal rod length (in mm)
    diagonal = model_prop("diagonal", float, 0)

    # Deviation of the ideal endstop position (in mm)
    endstop_adjustment = model_prop("endstop_adjustment", float, 0)

    # X coordinate of this tower (in mm)
    x_pos = model_prop("x_pos", float, 0)

    # Y coordinate of this tower (in mm)
    y_pos = model_prop("y_pos", float, 0)

    def __init__(self):
        super().__init__()
        self._angle_correction = 0
        self._diagonal = 0
        self._endstop_adjustment = 0
        self._x_pos = 0
        self._y_pos = 0
