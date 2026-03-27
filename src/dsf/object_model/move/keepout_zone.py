from typing import List

from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import model_prop


class KeepoutZoneCoordinates(ModelObject):
    """Coordinates of a keep-out zone"""

    # Maximum axis coordinate
    max = model_prop("max", float, 0)

    # Minimum axis coordinate
    min = model_prop("min", float, 0)

    def __init__(self):
        super().__init__()


class KeepoutZone(ModelObject):
    """Information about a configured keep-out zone"""

    # Indicates if this keep-out zone is enabled
    active = model_prop("active", bool, True)

    # Minimum and maximum coordinates of this zone
    coords = model_prop("coords", ModelCollection[KeepoutZoneCoordinates], ModelCollection(KeepoutZoneCoordinates))

    def __init__(self):
        super().__init__()
