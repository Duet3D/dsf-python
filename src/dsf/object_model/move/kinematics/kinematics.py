from typing import Union

from .kinematics_name import KinematicsName
from ..move_segmentation import MoveSegmentation
from ...model_object import ModelObject


class Kinematics(ModelObject):
    """Information about the configured geometry"""

    def __init__(self, name: KinematicsName = KinematicsName.unknown):
        super().__init__()
        self._name = name
        self._segmentation = None

    @staticmethod
    def get_kinematics_type(name: KinematicsName):
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
            name = KinematicsName(name)
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
        elif name == KinematicsName.delta:
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

    @property
    def name(self) -> KinematicsName:
        """Name of the configured kinematics"""
        return self._name

    @property
    def segmentation(self) -> Union[MoveSegmentation, None]:
        """Segmentation parameters or null if not configured"""
        return self._segmentation

    @segmentation.setter
    def segmentation(self, value):
        if value is None or isinstance(value, MoveSegmentation):
            self._segmentation = value
        elif isinstance(value, dict):  # Update from JSON
            if self._segmentation is None:
                self._segmentation = MoveSegmentation.from_json(value)
            else:
                self._segmentation.update_from_json(value)
        else:
            raise TypeError(f"{__name__}.segmentation must be None or of type MoveSegmentation."
                            f"Got {type(value)}: {value}")

    def _update_from_json(self, **kwargs):
        """Override ObjectModel._update_from_json to return the Kinematics type matching the given name"""
        if 'name' in kwargs and self.name != KinematicsName(kwargs.get('name')):
            kinematic_type = self.get_kinematics_type(kwargs.get('name'))
            new_kinematic = kinematic_type.update_from_json(kwargs)
            return new_kinematic

        super(Kinematics, self)._update_from_json(**kwargs)
        return self
