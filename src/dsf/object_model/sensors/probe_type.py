from enum import IntEnum


class ProbeType(IntEnum):
    """Supported probe types"""

    # No probe
    NoProbe = 0,

    # A simple unmodulated probe (like dc42's infrared probe)
    Analog = 1,

    # A modulated probe (like the original one shipped with the RepRapPro Ormerod)
    DumbModulated = 2,

    # Alternate analog probe (like the ultrasonic probe)
    AlternateAnalog = 3,

    # ndstop switch (obsolete, should not be used any more)
    EndstopSwitch_Obsolete = 4,

    # A switch that is triggered when the probe is activated (filtered)
    Digital = 5,

    # Endstop switch on the E1 endstop pin (obsolete, should not be used any more)
    E1Switch_Obsolete = 6,

    # Endstop switch on Z endstop pin (obsolete, should not be used any more)
    ZSwitch_Obsolete = 7,

    # A switch that is triggered when the probe is activated (unfiltered)
    UnfilteredDigital = 8,

    # A BLTouch probe
    BLTouch = 9,

    # Z motor stall detection
    ZMotorStall = 10
