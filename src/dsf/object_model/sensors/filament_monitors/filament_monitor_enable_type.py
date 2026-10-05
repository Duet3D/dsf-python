from enum import IntEnum

from ....utils import DeprecatedAliasEnumType


class FilamentMonitorEnableMode(IntEnum, metaclass=DeprecatedAliasEnumType):
    """Enumeration of supported filament sensors"""

    # Filament monitor is disabled
    DISABLED = 0

    # Filament monitor is enabled during prints from SD card
    ENABLED = 1

    # Filament monitor is always enabled (when printing from USB)
    ALWAYS_ENABLED = 2

    # Previous names, deprecated
    AlwaysEnabled = ALWAYS_ENABLED
    Disabled = DISABLED
    Enabled = ENABLED
