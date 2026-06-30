from typing import Union

from .kinematics_name import KinematicsName
from ..move_segmentation import MoveSegmentation
from ...model_object import ModelObject
from ...utils import model_prop, nullable_model_prop


class Kinematics(ModelObject):
    """Information about the configured geometry"""

    name = model_prop("name", KinematicsName, KinematicsName.unknown)
    segmentation = nullable_model_prop("segmentation", MoveSegmentation)

    def __init__(self, name: KinematicsName = KinematicsName.unknown):
        super().__init__()
        self._name = name
        self._segmentation = None

    @staticmethod
    def get_kinematics_type(name: KinematicsName | str):
        from .core_kinematics import CoreKinematics
        from .delta_kinematics import DeltaKinematics
        from .hangprinter_kinematics import HangprinterKinematics
        from .polar_kinematics import PolarKinematics
        from .scara_kinematics import ScaraKinematics
        """
        Figure out the required type for the given kinematics name
        :param name: Kinematics name
        :returns: Required type
        """
        if isinstance(name, str):
            name = KinematicsName(name.lower().replace(' ', ''))
        elif not isinstance(name, KinematicsName):
            raise TypeError(f'{__name__} must be KinematicsName. Got {type(name)}: {name}')

        if name in [
            KinematicsName.cartesian,
            KinematicsName.coreXY,
            KinematicsName.coreXYU,
            KinematicsName.coreXYUV,
            KinematicsName.coreXZ,
            KinematicsName.markForged
        ]:
            return CoreKinematics(name)
        elif name == KinematicsName.linearDelta:
            return DeltaKinematics(name)
        elif name == KinematicsName.rotaryDelta:
            return Kinematics(name)
        elif name == KinematicsName.hangprinter:
            return HangprinterKinematics()
        elif name in [KinematicsName.fiveBarScara, KinematicsName.scara]:
            return ScaraKinematics(name)
        elif name == KinematicsName.polar:
            return PolarKinematics()
        return name

    def _update_from_json(self, **kwargs):
        """Override ObjectModel._update_from_json to return the Kinematics type matching the given name"""
        if 'name' in kwargs:
            kwargs['name'] = KinematicsName(kwargs.get('name').lower().replace(' ', ''))

            if self.name != kwargs.get('name'):
                kinematic_type = self.get_kinematics_type(kwargs.get('name'))
                new_kinematic = kinematic_type.update_from_json(kwargs)
                return new_kinematic

        super(Kinematics, self)._update_from_json(**kwargs)
        return self
