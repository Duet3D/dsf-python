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
    linearDelta = "delta"
    polar = "polar"
    rotaryDelta = "rotarydelta"
    scara = "scara"
    unknown = "unknown"
