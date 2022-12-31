from .kinematics import Kinematics
from .kinematics_name import KinematicsName
from .tilt_correction import TiltCorrection


class ZLeadscrewKinematics(Kinematics):
    """Base kinematics class that provides the ability to level the bed using Z leadscrews"""
    def __init__(self, name: KinematicsName):
        super(ZLeadscrewKinematics, self).__init__(name)
        # Parameters describing the tilt correction
        self._tilt_correction = TiltCorrection()
        
    @property
    def tilt_correction(self):
        """Parameters describing the tilt correction"""
        return self._tilt_correction
