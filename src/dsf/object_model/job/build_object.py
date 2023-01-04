from __future__ import annotations

from ..model_object import ModelObject


class BuildObject(ModelObject):
    """Information about a detected build object"""

    def __init__(self):
        super().__init__()
        # Indicates if this build object is cancelled
        self._canceled = False
        # Name of the build object (if any)
        self._name = None
        # X coordinates of the build object (in mm or None if not found)
        self._x = None
        # Y coordinates of the build object (in mm or None if not found)
        self._y = None

    @property
    def canceled(self) -> bool:
        """Indicates if this build object is cancelled"""
        return self._canceled

    @canceled.setter
    def canceled(self, value: bool):
        self._canceled = bool(value)

    @property
    def name(self) -> str | None:
        """Name of the build object (if any)"""
        return self._name

    @name.setter
    def name(self, value: str | None = None):
        self._name = str(value) if value is not None else None

    @property
    def x(self) -> list[float | None] | None:
        """X coordinates of the build object (in mm or None if not found)"""
        return self._x

    @property
    def y(self) -> list[float | None] | None:
        """Y coordinates of the build object (in mm or None if not found)"""
        return self._y
