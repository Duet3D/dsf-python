from enum import Enum


class FileDirectory(str, Enum):
    """Base file directory for lookups"""

    # Filaments directory
    FILAMENTS = "Filaments"

    # Firmware directory
    FIRMWARE = "Firmware"

    # GCodes directory
    GCODES = "GCodes"

    # Macros directory
    MACROS = "Macros"

    # Menu directory
    MENU = "Menu"

    # System directory
    SYSTEM = "System"

    # WWW directory
    WEB = "Web"
