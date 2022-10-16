from .kinematics_base import KinematicsBase
from .kinematics_name import KinematicsName


class PolarKinematics(KinematicsBase):
    """
    Kinematics class for polar kinematics
    """

    def __init__(self):
        super(PolarKinematics, self).__init__()
        self.name = KinematicsName.polar
