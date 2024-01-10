from enum import IntEnum


class FilamentMonitorEnableMode(IntEnum):
    """Enumeration of supported filament sensors"""

    # Filament monitor is disabled
    Disabled = 0

    # Filament monitor is enabled during prints from SD card
    Enabled = 1

    # Filament monitor is always enabled (when printing from USB)
    AlwaysEnabled = 2
