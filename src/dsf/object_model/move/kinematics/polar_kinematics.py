from .kinematics import Kinematics
from .kinematics_name import KinematicsName
from ...utils import model_prop


class PolarKinematics(Kinematics):
    """
    Kinematics class for polar kinematics
    """

    # Homed radius (in mm)
    radius_homed = model_prop("radius_homed", float, 0.0)

    #Maximum radius (in mm)
    radius_max = model_prop("radius_max", float, 0.0)

    # Minimum radius (in mm)
    radius_min = model_prop("radius_min", float, 0.0)

    # Maximum turntable acceleration (in mm/s^2)
    tt_acc_max = model_prop("tt_acc_max", float, 0.0)

    # Maxmimum turntable speed (in mm/s)
    tt_speed_max = model_prop("tt_speed_max", float, 0.0)

    def __init__(self):
        super(PolarKinematics, self).__init__()
        self._name = KinematicsName.polar

