from enum import Enum

from ...utils import DeprecatedAliasEnumType


class EndstopType(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Type of configured endstop"""

    # Generic input pin
    INPUT_PIN = "inputPin"

    # Z-probe acts as an endstop
    Z_PROBE_AS_ENDSTOP = "zProbeAsEndstop"

    # Motor stall detection stops all the drives when triggered
    MOTOR_STALL_ANY = "motorStallAny"

    # Motor stall detection stops individual drives when triggered
    MOTOR_STALL_INDIVIDUAL = "motorStallIndividual"

    # Encoder position error stops all the drives when triggered
    MOTOR_STALL_ENCODER = "motorStallEncoder"

    # Unknown
    UNKNOWN = "unknown"

    # Previous names, deprecated
    InputPin = INPUT_PIN
    MotorStallAny = MOTOR_STALL_ANY
    MotorStallEncoder = MOTOR_STALL_ENCODER
    MotorStallIndividual = MOTOR_STALL_INDIVIDUAL
    Unknown = UNKNOWN
    ZProbeAsEndstop = Z_PROBE_AS_ENDSTOP
