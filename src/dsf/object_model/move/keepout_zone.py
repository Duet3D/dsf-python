from typing import List

from ..model_collection import ModelCollection
from ..model_object import ModelObject


class KeepoutZoneCoordinates(ModelObject):
    """Coordinates of a keep-out zone"""

    def __init__(self):
        super().__init__()
        # Maximum axis coordinate
        self._max = 0
        # Minimum axis coordinate
        self._min = 0

    @property
    def max(self) -> float:
        """Maximum axis coordinate"""
        return self._max

    @max.setter
    def max(self, value):
        self._max = float(value)

    @property
    def min(self) -> float:
        """Minimum axis coordinate"""
        return self._min

    @min.setter
    def min(self, value):
        self._min = float(value)


class KeepoutZone(ModelObject):
    """Information about a configured keep-out zone"""

    def __init__(self):
        super().__init__()
        # Indicates if this keep-out zone is enabled
        self._active = True
        # Minimum and maximum coordinates of this zone
        self._coords = ModelCollection(KeepoutZoneCoordinates)

    @property
    def active(self) -> bool:
        """Minimum axis coordinate"""
        return self._active

    @active.setter
    def active(self, value):
        self._active = bool(value)

    @property
    def coords(self) -> List[KeepoutZoneCoordinates]:
        """Minimum and maximum coordinates of this zone"""
        return self._coords
