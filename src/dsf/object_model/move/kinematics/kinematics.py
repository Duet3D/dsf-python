from .kinematics_base import KinematicsBase
from .kinematics_name import KinematicsName
from .utils import get_kinematics_type


class Kinematics(KinematicsBase):
    """
    Information about the configured geometry
    See KinematicsBase class
    """

    def __init__(self, name: KinematicsName = KinematicsName.unknown):
        super(Kinematics, self).__init__(name)

    def _update_from_json(self, **kwargs) -> 'Kinematics':
        """Override ObjectModel._update_from_json to return the Kinematics type matching the given name"""
        super(Kinematics, self)._update_from_json(**kwargs)
        kinematic_type = get_kinematics_type(kwargs.get('name'))
        return kinematic_type.from_json(kwargs)
