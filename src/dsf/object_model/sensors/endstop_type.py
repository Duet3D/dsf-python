from enum import Enum


class EndstopType(str, Enum):
    """Type of configured endstop"""

    # Generic input pin
    InputPin = "inputPin"

    # Z-probe acts as an endstop
    ZProbeAsEndstop = "zProbeAsEndstop"

    # Motor stall detection stops all the drives when triggered
    MotorStallAny = "motorStallAny"

    # Motor stall detection stops individual drives when triggered
    MotorStallIndividual = "motorStallIndividual"

    # Unknown
    Unknown = "unknown"
