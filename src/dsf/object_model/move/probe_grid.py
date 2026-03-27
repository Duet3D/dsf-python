from ..model_object import ModelObject
from ..model_collection import ModelCollection
from ..utils import model_prop


class ProbeGrid(ModelObject):
    """Information about the configured probe grid (see M557)"""

    # Axis letters of this heightmap
    axes = model_prop("axes", ModelCollection[str], ModelCollection(str, ['X', 'Y']))

    # End coordinates of the heightmap
    maxs = model_prop("maxs", ModelCollection[float], ModelCollection(float, [-1.0, -1.0]))

    # Start coordinates of the heightmap
    mins = model_prop("mins", ModelCollection[float], ModelCollection(float, [0.0, 0.0]))

    # Probing radius for delta kinematics
    radius = model_prop("radius", float)

    # Spacings between the coordinates
    spacings = model_prop("spacings", ModelCollection[float], ModelCollection(float, [0.0, 0.0]))

    def __init__(self):
        super().__init__()
