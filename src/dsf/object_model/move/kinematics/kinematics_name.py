from enum import Enum


class KinematicsName(str, Enum):
    """Enumeration of supported kinematics, the values are the names written by DSF"""

    cartesian = "cartesian"
    coreXY = "coreXY"
    coreXYU = "coreXYU"
    coreXYUV = "coreXYUV"
    coreXZ = "coreXZ"
    markForged = "markForged"
    fiveBarScara = "FiveBarScara"
    hangprinter = "Hangprinter"
    linearDelta = "delta"
    polar = "Polar"
    rotaryDelta = "Rotary delta"
    scara = "Scara"
    unknown = "unknown"

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
            return cls.linearDelta
        if name == "rotarydelta":
            return cls.rotaryDelta
        return cls.unknown
