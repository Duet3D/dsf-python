from typing import List

from .kinematics_base import KinematicsBase
from .kinematics_name import KinematicsName


class HangprinterKinematics(KinematicsBase):
    """Information about hangprinter kinematics"""
    def __init__(self):
        super(HangprinterKinematics, self).__init__()
        self.name = KinematicsName.hangprinter
        # Anchor configurations for A, B, C, Dz
        self._anchors = [
            [0,     -2000, -100],
            [2000,   1000, -100],
            [-2000,  1000, -100],
            [0,      0,    3000]
        ]
        self._print_radius = 1500

    @property
    def anchors(self) -> List[List[float]]:
        """Anchor configurations for A, B, C, Dz"""
        return self._anchors
    
    @property
    def print_radius(self) -> float:
        """Print radius (in mm)"""
        return self._print_radius
    
    @print_radius.setter
    def print_radius(self, value):
        self._print_radius = float(value) if value is not None else 0

    def _update_from_json(self, **kwargs) -> 'HangprinterKinematics':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(HangprinterKinematics, self)._update_from_json(**kwargs)
        self._anchors = [[int(x) for x in y] for y in kwargs.get('anchors', [])]
        return self
