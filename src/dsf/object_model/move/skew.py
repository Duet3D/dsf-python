from ..model_object import ModelObject
from ..utils import model_prop


class Skew(ModelObject):
    """Class holding details about orthogonoal axis compensation parameters"""

    # Indicates if the TanXY value is used to compensate X when Y moves (else Y when X moves)
    compensate_XY = model_prop("compensate_XY", bool, True)

    # Tangent of the skew angle for the XY or YX axes
    tan_XY = model_prop("tan_XY", float, 0)

    # Tangent of the skew angle for the XZ axes
    tan_XZ = model_prop("tan_XZ", float, 0)

    # Tangent of the skew angle for the YZ axes
    tan_YZ = model_prop("tan_YZ", float, 0)

    def __init__(self):
        super().__init__()
