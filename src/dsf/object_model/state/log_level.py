from enum import Enum


class LogLevel(str, Enum):
    """Class representing the configured log level"""

    # Log everything including debug messages
    Debug = "debug"

    # Log information and warning messages
    Info = "info"

    # Log warning messages only
    Warn = "warn"

    # Logging is disabled
    Off = "off"
