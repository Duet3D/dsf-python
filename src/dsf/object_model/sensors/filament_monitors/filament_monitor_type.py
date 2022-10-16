from enum import Enum


class FilamentMonitorType(str, Enum):
    """Enumeration of supported filament sensors"""

    # Simple filament sensor
    Simple = "simple"

    # Laser filament sensor
    Laser = "laser"

    # Pulsed filament sensor
    Pulsed = "pulsed"

    # Rotating magnet filament sensor
    RotatingMagnet = "rotatingMagnet"

    # Unknown sensor type
    Unknown = "unknown"
