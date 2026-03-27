from .kinematics import Kinematics
from .kinematics_name import KinematicsName
from .tilt_correction import TiltCorrection
from ...utils import model_prop


class ZLeadscrewKinematics(Kinematics):
    """Base kinematics class that provides the ability to level the bed using Z leadscrews"""

    # Parameters describing the tilt correction
    tilt_correction = model_prop("tilt_correction", TiltCorrection)

    def __init__(self, name: KinematicsName):
        super(ZLeadscrewKinematics, self).__init__(name)
