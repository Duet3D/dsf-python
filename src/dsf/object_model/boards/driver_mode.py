from enum import Enum


class DriverMode(int, Enum):
    """State of a channel"""

    # Constant off-time chopper
    constantOffTime = 0,

    # Random off-time chopper
    randomOffTime = 1,

    # SpreadCycle
    spreadCycle = 2,

    # StealthChop (includes stealthChop2)
    stealthChop = 3,

    # Field-oriented control (direct)
    direct = 4,

    # Driver mode is unknown
    unknown = 5
