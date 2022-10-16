from typing import List

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
    def axes(self) -> List[str]:
        """Axis letters of this heightmap"""
        return self._axes

    @property
    def maxs(self) -> List[float]:
        """End coordinates of the heightmap"""
        return self._maxs

    @property
    def mins(self) -> List[float]:
        """Start coordinates of the heightmap"""
        return self._mins

    @property
    def radius(self) -> float:
        """Probing radius for delta kinematics"""
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = float(value) if value is not None else 0

    @property
    def spacings(self) -> List[float]:
        """Spacings between the coordinates"""
        return self._spacings

    def _update_from_json(self, **kwargs) -> 'ProbeGrid':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(ProbeGrid, self)._update_from_json(**kwargs)
        self._axes = [str(letter) for letter in kwargs.get('axes', ['X', 'Y'])]
        self._maxs = [float(value) for value in kwargs.get('maxs', [-1, -1])]
        self._mins = [float(value) for value in kwargs.get('mins', [0, 0])]
        self._spacings = [float(value) for value in kwargs.get('spacings', [0, 0])]
        return self
