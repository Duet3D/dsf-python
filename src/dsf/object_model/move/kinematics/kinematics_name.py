from enum import Enum


class KinematicsName(str, Enum):
    """Enumeration of supported kinematics"""

    cartesian = "cartesian"
    coreXY = "corexy"
    coreXYU = "corexyu"
    coreXYUV = "corexyuv"
    coreXZ = "corexz"
    markForged = "markforged"
    fiveBarScara = "fivebarscara"
    hangprinter = "hangprinter"
    delta = "delta"
    polar = "polar"
    rotaryDelta = "rotary delta"
    scara = "scara"
    unknown = "unknown"
