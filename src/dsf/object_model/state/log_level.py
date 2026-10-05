from enum import Enum

from ...utils import DeprecatedAliasEnumType


class LogLevel(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Class representing the configured log level"""

    # Log everything including debug messages
    DEBUG = "debug"

    # Log information and warning messages
    INFO = "info"

    # Log warning messages only
    WARN = "warn"

    # Logging is disabled
    OFF = "off"

    # Previous names, deprecated
    Debug = DEBUG
    Info = INFO
    Off = OFF
    Warn = WARN
