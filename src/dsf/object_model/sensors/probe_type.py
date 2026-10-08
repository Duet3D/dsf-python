from enum import IntEnum

from ...utils import DeprecatedAliasEnumType


class ProbeType(IntEnum, metaclass=DeprecatedAliasEnumType):
    """Supported probe types"""

    # No probe
    NONE = 0

    # A simple unmodulated probe (like dc42's infrared probe)
    ANALOG = 1

    # A modulated probe (like the original one shipped with the RepRapPro Ormerod)
    DUMB_MODULATED = 2

    # Alternate analog probe (obsolete, should not be used anymore)
    ALTERNATE_ANALOG_OBSOLETE = 3

    # Endstop switch (obsolete, should not be used anymore)
    ENDSTOP_SWITCH_OBSOLETE = 4

    # A switch that is triggered when the probe is activated (filtered)
    DIGITAL = 5

    # Endstop switch on the E1 endstop pin (obsolete, should not be used anymore)
    E1_SWITCH_OBSOLETE = 6

    # Endstop switch on Z endstop pin (obsolete, should not be used anymore)
    Z_SWITCH_OBSOLETE = 7

    # A switch that is triggered when the probe is activated (unfiltered)
    UNFILTERED_DIGITAL = 8

    # A BLTouch probe
    BLTOUCH = 9

    # Z motor stall detection
    Z_MOTOR_STALL = 10

    # Analog scanning probe
    SCANNING_ANALOG = 11

    # Deprecated alias of ScanningAnalog
    ScanningZProbe = 11

    # Load cell probe measuring the contact force
    LOAD_CELL = 12

    # Previous names, deprecated
    Analog = ANALOG
    BLTouch = BLTOUCH
    Digital = DIGITAL
    DumbModulated = DUMB_MODULATED
    E1Switch_Obsolete = E1_SWITCH_OBSOLETE
    EndstopSwitch_Obsolete = ENDSTOP_SWITCH_OBSOLETE
    LoadCell = LOAD_CELL
    NoProbe = NONE
    ScanningAnalog = SCANNING_ANALOG
    UnfilteredDigital = UNFILTERED_DIGITAL
    ZMotorStall = Z_MOTOR_STALL
    ZSwitch_Obsolete = Z_SWITCH_OBSOLETE
