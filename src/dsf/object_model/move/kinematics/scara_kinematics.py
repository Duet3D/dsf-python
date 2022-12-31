from .kinematics_name import KinematicsName
from .zleadscrew_kinematics import ZLeadscrewKinematics


class ScaraKinematics(ZLeadscrewKinematics):
    """
    Kinematics class for SCARA kinematics
    """

    def __init__(self, name: KinematicsName):
        super(ScaraKinematics, self).__init__(name)

