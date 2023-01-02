from enum import Enum


class KinematicsName(str, Enum):
    """Enumeration of supported kinematics"""

    cartesian = "cartesian"
    coreXY = "coreXY"
    coreXYU = "coreXYU"
    coreXYUV = "coreXYUV"
    coreXZ = "coreXZ"
    markForged = "markForged"
    fiveBarScara = "fiveBarScara"
    hangprinter = "hangprinter"
    delta = "delta"
    polar = "polar"
    rotaryDelta = "rotaryDelta"
    scara = "scara"
    unknown = "unknown"
