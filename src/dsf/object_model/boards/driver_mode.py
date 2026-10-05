from enum import Enum

from ...utils import DeprecatedAliasEnumType


class DriverMode(int, Enum, metaclass=DeprecatedAliasEnumType):
    """State of a channel"""

    # Constant off-time chopper
    CONSTANT_OFF_TIME = (0,)

    # Random off-time chopper
    RANDOM_OFF_TIME = (1,)

    # SpreadCycle
    SPREAD_CYCLE = (2,)

    # StealthChop (includes stealthChop2)
    STEALTH_CHOP = (3,)

    # Field-oriented control (direct)
    DIRECT = (4,)

    # Assisted open loop
    ASSISTED_OPEN = (5,)

    # Driver mode is unknown
    UNKNOWN = 6

    # Previous names, deprecated
    assistedOpen = ASSISTED_OPEN
    constantOffTime = CONSTANT_OFF_TIME
    direct = DIRECT
    randomOffTime = RANDOM_OFF_TIME
    spreadCycle = SPREAD_CYCLE
    stealthChop = STEALTH_CHOP
    unknown = UNKNOWN
