from enum import Enum


class EndstopType(str, Enum):
    """Type of configured endstop"""

    # Generic input pin
    InputPin = "InputPin"

    # Z-probe acts as an endstop
    ZProbeAsEndstop = "ZProbeAsEndstop"

    # Motor stall detection stops all the drives when triggered
    MotorStallAny = "MotorStallAny"

    # Motor stall detection stops individual drives when triggered
    MotorStallIndividual = "MotorStallIndividual"

    # Unknown
    Unknown = "Unknown"
