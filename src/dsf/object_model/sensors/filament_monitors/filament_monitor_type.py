from enum import Enum

from ....utils import DeprecatedAliasEnumType


class FilamentMonitorType(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Enumeration of supported filament sensors"""

    # Simple filament sensor
    SIMPLE = "simple"

    # Laser filament sensor
    LASER = "laser"

    # Pulsed filament sensor
    PULSED = "pulsed"

    # Rotating magnet filament sensor
    ROTATING_MAGNET = "rotatingMagnet"

    # Unknown sensor type
    UNKNOWN = "unknown"

    # Previous names, deprecated
    Laser = LASER
    Pulsed = PULSED
    RotatingMagnet = ROTATING_MAGNET
    Simple = SIMPLE
    Unknown = UNKNOWN
