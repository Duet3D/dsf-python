from ..model_object import ModelObject
from ..model_collection import ModelCollection
from ..utils import model_prop


class MoveRotation(ModelObject):
    """Information about centre rotation as defined by G68"""

    # Angle of the centre rotatation (in deg)
    angle = model_prop("angle", float, 0)

    # XY coordinates of the centre rotation
    centre = model_prop("centre", ModelCollection[float], ModelCollection(float, [0.0, 0.0]))

    def __init__(self):
        super().__init__()
