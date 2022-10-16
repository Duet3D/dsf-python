from enum import Enum


class Compatibility(str, Enum):
    """Compatibility level for emulation"""

    # No emulation (same as RepRapFirmware)
    Default = "Default"

    # Emulating RepRapFirmware
    RepRapFirmware = "RepRapFirmware"

    # Emulating Marlin
    Marlin = "Marlin"

    # Emulating Teacup
    Teacup = "Teacup"

    # Emulating Sprinter
    Sprinter = "Sprinter"

    # Emulating Repetier
    Repetier = "Repetier"

    # Emulating NanoDLP
    NanoDLP = "NanoDLP"
