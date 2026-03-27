from typing import List

from .delta_tower import DeltaTower
from .kinematics import Kinematics
from .kinematics_name import KinematicsName
from ...model_collection import ModelCollection
from ...utils import model_prop


class DeltaKinematics(Kinematics):
    """Delta kinematics"""

    # Delta radius (in mm)
    delta_radius = model_prop("delta_radius", float, 0.0)

    # Homed height of a delta printer in mm
    homed_height = model_prop("homed_height", float, 0.0)

    # Print radius for Hangprinter and Delta geometries (in mm)
    print_radius = model_prop("print_radius", float, 0.0)

    # Delta tower properties
    towers = model_prop("towers", ModelCollection[DeltaTower], ModelCollection(DeltaTower, [{}, {}, {}]))

    # How much Z needs to be raised for each unit of movement in the +X direction
    x_tilt = model_prop("x_tilt", float, 0.0)

    # How much Z needs to be raised for each unit of movement in the +Y direction
    y_tilt = model_prop("y_tilt", float, 0.0)

    def __init__(self, name: KinematicsName = KinematicsName.linearDelta):
        super().__init__(name)
