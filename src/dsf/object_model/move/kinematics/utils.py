from .core_kinematics import CoreKinematics
from .delta_kinematics import DeltaKinematics
from .hangprinter_kinematics import HangprinterKinematics
from .kinematics_base import KinematicsBase
from .kinematics_name import KinematicsName
from .polar_kinematics import PolarKinematics
from .scara_kinematics import ScaraKinematics


def get_kinematics_type(name: KinematicsName):
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
        return CoreKinematics
    elif name == KinematicsName.delta:
        return DeltaKinematics
    elif name == KinematicsName.hangprinter:
        return HangprinterKinematics
    elif name in [KinematicsName.fiveBarScara, KinematicsName.scara]:
        return ScaraKinematics
    elif name == KinematicsName.polar:
        return PolarKinematics
    return KinematicsBase
