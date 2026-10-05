from enum import Enum

from ..utils import DeprecatedAliasEnumType


class CodeChannel(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Enumeration of every available code channel"""

    # Code channel for HTTP requests
    HTTP = "HTTP"

    # Code channel for Telnet requests
    TELNET = "Telnet"

    # Code channel for primary file prints
    FILE = "File"

    # Code channel for USB requests
    USB = "USB"

    # Code channel for serial devices (e.g. PanelDue)
    AUX = "Aux"

    # Code channel for running triggers or config.g
    TRIGGER = "Trigger"

    # Code channel for the code queue that executes a couple of codes in-sync with moves of the primary print file
    QUEUE = "Queue"

    # Code channel for auxiliary LCD devices (e.g. PanelOne)
    LCD = "LCD"

    # Default code channel for requests over SPI
    SBC = "SBC"

    # Code channel that executes the daemon process
    DAEMON = "Daemon"

    # Code channel for the second UART port
    AUX2 = "Aux2"

    # Code channel that executes macros on power fail, heater faults and filament out
    AUTOPAUSE = "Autopause"

    # Code channel for secondary file prints
    FILE2 = "File2"

    # Code channel for the code queue that executes a couple of codes in-sync with moves of the primary print file
    QUEUE2 = "Queue2"

    # Code channel for secondary USB requests
    USB2 = "USB2"

    # Unknown code channel
    UNKNOWN = "Unknown"

    # Default channel for codes sent by dsf-python
    DEFAULT_CHANNEL = SBC
    __kept_aliases__ = ("DEFAULT_CHANNEL",)

    # Previous names, deprecated
    Autopause = AUTOPAUSE
    Aux = AUX
    Aux2 = AUX2
    Daemon = DAEMON
    File = FILE
    File2 = FILE2
    Queue = QUEUE
    Queue2 = QUEUE2
    Telnet = TELNET
    Trigger = TRIGGER
    Unknown = UNKNOWN

    @staticmethod
    def list():
        return list(map(lambda cc: cc, CodeChannel))

    def get_input_index(self) -> int:
        """Get the index of this code channel for use in client init messages"""
        return self.list().index(self)
