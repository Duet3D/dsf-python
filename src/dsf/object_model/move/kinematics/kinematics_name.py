from enum import Enum

from ....utils import DeprecatedAliasEnumType


class KinematicsName(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Enumeration of supported kinematics, the values are the names written by DSF"""

    CARTESIAN = "cartesian"
    CORE_XY = "coreXY"
    CORE_XYU = "coreXYU"
    CORE_XYUV = "coreXYUV"
    CORE_XZ = "coreXZ"
    MARKFORGED = "markForged"
    FIVE_BAR_SCARA = "FiveBarScara"
    HANGPRINTER = "Hangprinter"
    LINEAR_DELTA = "delta"
    POLAR = "Polar"
    ROTARY_DELTA = "Rotary delta"
    SCARA = "Scara"
    UNKNOWN = "unknown"

    # Previous names, deprecated
    cartesian = CARTESIAN
    coreXY = CORE_XY
    coreXYU = CORE_XYU
    coreXYUV = CORE_XYUV
    coreXZ = CORE_XZ
    fiveBarScara = FIVE_BAR_SCARA
    hangprinter = HANGPRINTER
    linearDelta = LINEAR_DELTA
    markForged = MARKFORGED
    polar = POLAR
    rotaryDelta = ROTARY_DELTA
    scara = SCARA
    unknown = UNKNOWN

    @classmethod
    def _missing_(cls, value: object):
        # Like DSF, names are case-insensitive, "lineardelta" and "rotarydelta" are accepted as well
        # and any other name is unknown
        if not isinstance(value, str):
            return None
        name = value.lower()
        for member in cls:
            if member.value.lower() == name:
                return member
        if name == "lineardelta":
            return cls.LINEAR_DELTA
        if name == "rotarydelta":
            return cls.ROTARY_DELTA
        return cls.UNKNOWN
