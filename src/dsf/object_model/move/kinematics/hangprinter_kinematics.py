from typing import List

from .kinematics import Kinematics
from .kinematics_name import KinematicsName


class HangprinterKinematics(Kinematics):
    """Information about hangprinter kinematics"""
    def __init__(self):
        super(HangprinterKinematics, self).__init__()
        self._name = KinematicsName.hangprinter
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
        self._print_radius = float(value)
