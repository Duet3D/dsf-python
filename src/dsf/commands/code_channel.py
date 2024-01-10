from enum import Enum


class CodeChannel(str, Enum):
    """Enumeration of every available code channel"""

    # Code channel for HTTP requests
    HTTP = "HTTP"

    # Code channel for Telnet requests
    Telnet = "Telnet"

    # Code channel for primary file prints
    File = "File"

    # Code channel for USB requests
    USB = "USB"

    # Code channel for serial devices (e.g. PanelDue)
    Aux = "Aux"

    # Code channel for running triggers or config.g
    Trigger = "Trigger"

    # Code channel for the code queue that executes a couple of codes in-sync with moves of the primary print file
    Queue = "Queue"

    # Code channel for auxiliary LCD devices (e.g. PanelOne)
    LCD = "LCD"

    # Default code channel for requests over SPI
    SBC = "SBC"

    # Code channel that executes the daemon process
    Daemon = "Daemon"

    # Code channel for the second UART port
    Aux2 = "Aux2"

    # Code channel that executes macros on power fail, heater faults and filament out
    Autopause = "Autopause"

    # Code channel for secondary file prints
    File2 = "File2"

    # Code channel for the code queue that executes a couple of codes in-sync with moves of the primary print file
    Queue2 = "Queue2"

    # Unknown code channel
    Unknown = "Unknown"

    DEFAULT_CHANNEL = SBC

    @staticmethod
    def list():
        return list(map(lambda cc: cc.value, CodeChannel))
