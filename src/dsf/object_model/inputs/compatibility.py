from enum import Enum

from ...utils import DeprecatedAliasEnumType


class Compatibility(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Compatibility level for emulation"""

    # No emulation (same as RepRapFirmware)
    DEFAULT = "Default"

    # Emulating RepRapFirmware
    REPRAPFIRMWARE = "RepRapFirmware"

    # Emulating Marlin
    MARLIN = "Marlin"

    # Emulating Teacup
    TEACUP = "Teacup"

    # Emulating Sprinter
    SPRINTER = "Sprinter"

    # Emulating Repetier
    REPETIER = "Repetier"

    # Emulating NanoDLP
    NANODLP = "NanoDLP"

    # Previous names, deprecated
    Default = DEFAULT
    Marlin = MARLIN
    NanoDLP = NANODLP
    RepRapFirmware = REPRAPFIRMWARE
    Repetier = REPETIER
    Sprinter = SPRINTER
    Teacup = TEACUP
