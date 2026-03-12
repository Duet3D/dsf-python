from typing import List

from ..model_object import ModelObject


class BuildObject(ModelObject):
    """Information about a detected build object"""

    def __init__(self) -> None:
        super().__init__()
        # Indicates if this build object is cancelled
        self._canceled: bool = False
        # Name of the build object (if any)
        self._name: str | None = None
        # X coordinates of the build object (in mm or null if not found)
        self._x: List[float] | None = None
        # Y coordinates of the build object (in mm or null if not found)
        self._y: List[float] | None = None

    @property
    def canceled(self) -> bool:
        """Indicates if this build object is cancelled"""
        return self._canceled

    @canceled.setter
    def canceled(self, value: bool | int | str):
        self._canceled = bool(value)

    @property
    def name(self) -> str | None:
        """Name of the build object (if any)"""
        return self._name

    @name.setter
    def name(self, value: str | None):
        self._name = str(value) if value is not None else None

    @property
    def x(self) -> List[float] | None:
        """X coordinates of the build object (in mm or null if not found)"""
        return self._x

    @property
    def y(self) -> List[float] | None:
        """Y coordinates of the build object (in mm or null if not found)"""
        return self._y
