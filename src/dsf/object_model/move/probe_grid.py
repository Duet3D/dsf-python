from __future__ import annotations

from ..model_object import ModelObject


class ProbeGrid(ModelObject):
    """Information about the configured probe grid (see M557)"""
    def __init__(self):
        super().__init__()
        # Axis letters of this heightmap
        self._axes = ['X', 'Y']
        # End coordinates of the heightmap
        self._maxs = [-1, -1]
        # Start coordinates of the heightmap
        self._mins = [0, 0]
        # Probing radius for delta kinematics
        self._radius = 0
        # Spacings between the coordinates
        self._spacings = [0, 0]

    @property
    def axes(self) -> list[str]:
        """Axis letters of this heightmap"""
        return self._axes

    @property
    def maxs(self) -> list[float]:
        """End coordinates of the heightmap"""
        return self._maxs

    @property
    def mins(self) -> list[float]:
        """Start coordinates of the heightmap"""
        return self._mins

    @property
    def radius(self) -> float:
        """Probing radius for delta kinematics"""
        return self._radius

    @radius.setter
    def radius(self, value: float):
        self._radius = float(value)

    @property
    def spacings(self) -> list[float]:
        """Spacings between the coordinates"""
        return self._spacings
