from typing import List

from .kinematics import Kinematics
from .kinematics_name import KinematicsName
from ...utils import model_prop


class HangprinterKinematics(Kinematics):
    """Information about hangprinter kinematics"""

    anchors = model_prop("anchors", list[list[float]], [
            [0,     -2000, -100],
            [2000,   1000, -100],
            [-2000,  1000, -100],
            [0,      0,    3000]
        ])
    print_radius = model_prop("print_radius", float, 1500)

    def __init__(self):
        super(HangprinterKinematics, self).__init__()
        self.name = KinematicsName.hangprinter

