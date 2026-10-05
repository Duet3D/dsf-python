from .kinematics_name import KinematicsName
from ..move_segmentation import MoveSegmentation
from ...model_object import ModelObject
from ...utils import model_prop, nullable_model_prop
from ....utils import JSONElement


class Kinematics(ModelObject):
    """Information about the configured geometry"""

    name = model_prop("name", KinematicsName, KinematicsName.UNKNOWN)
    segmentation = nullable_model_prop("segmentation", MoveSegmentation)

    def __init__(self, name: KinematicsName = KinematicsName.UNKNOWN):
        super().__init__()
        self._name = name
        self._segmentation = None

    @staticmethod
    def get_kinematics_type(name: KinematicsName | str) -> "Kinematics":
        """
        Figure out the required type for the given kinematics name
        :param name: Kinematics name
        :returns: Required type
        """
        from .core_kinematics import CoreKinematics
        from .delta_kinematics import DeltaKinematics
        from .hangprinter_kinematics import HangprinterKinematics
        from .polar_kinematics import PolarKinematics
        from .scara_kinematics import ScaraKinematics

        name = KinematicsName(name)

        if name in [
            KinematicsName.CARTESIAN,
            KinematicsName.CORE_XY,
            KinematicsName.CORE_XYU,
            KinematicsName.CORE_XYUV,
            KinematicsName.CORE_XZ,
            KinematicsName.MARKFORGED,
        ]:
            return CoreKinematics(name)
        elif name == KinematicsName.LINEAR_DELTA:
            return DeltaKinematics(name)
        elif name == KinematicsName.ROTARY_DELTA:
            return Kinematics(name)
        elif name == KinematicsName.HANGPRINTER:
            return HangprinterKinematics()
        elif name in [KinematicsName.FIVE_BAR_SCARA, KinematicsName.SCARA]:
            return ScaraKinematics(name)
        elif name == KinematicsName.POLAR:
            return PolarKinematics()
        return Kinematics(name)

    def _update_from_json(self, **kwargs: JSONElement) -> "Kinematics":
        """Override ObjectModel._update_from_json to return the Kinematics type matching the given name"""
        name = kwargs.get("name")
        if isinstance(name, str):
            kinematics_name = KinematicsName(name)
            kwargs["name"] = kinematics_name

            if self.name != kinematics_name:
                return self.get_kinematics_type(kinematics_name).update_from_json(kwargs)

        super(Kinematics, self)._update_from_json(**kwargs)
        return self
