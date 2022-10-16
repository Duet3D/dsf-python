from .kinematics_base import KinematicsBase
from .tilt_correction import TiltCorrection


class ZLeadscrewKinematics(KinematicsBase):
    """Base kinematics class that provides the ability to level the bed using Z leadscrews"""
    def __init__(self):
        super(ZLeadscrewKinematics, self).__init__()
        # Parameters describing the tilt correction
        self._tilt_correction = TiltCorrection()
        
    @property
    def tilt_correction(self):
        """Parameters describing the tilt correction"""
        return self._tilt_correction

    def _update_from_json(self, **kwargs) -> 'ZLeadscrewKinematics':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(ZLeadscrewKinematics, self)._update_from_json(**kwargs)
        self._tilt_correction = TiltCorrection.from_json(kwargs.get('tiltCorrection'))
        return self
