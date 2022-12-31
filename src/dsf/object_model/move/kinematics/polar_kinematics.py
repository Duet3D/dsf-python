from .kinematics import Kinematics
from .kinematics_name import KinematicsName


class PolarKinematics(Kinematics):
    """
    Kinematics class for polar kinematics
    """

    def __init__(self):
        super(PolarKinematics, self).__init__()
        self._name = KinematicsName.polar

