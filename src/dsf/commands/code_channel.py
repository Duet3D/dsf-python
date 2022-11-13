from enum import Enum


class CodeChannel(str, Enum):
    """Enumeration of every available code channel"""

    HTTP = "HTTP"
    Telnet = "Telnet"
    File = "File"
    USB = "USB"
    Aux = "Aux"
    Trigger = "Trigger"
    Queue = "Queue"
    LCD = "LCD"
    SBC = "SBC"
    Daemon = "Daemon"
    Aux2 = "Aux2"
    Autopause = "Autopause"
    Unknown = "Unknown"

    DEFAULT_CHANNEL = SBC

    @staticmethod
    def list():
        return list(map(lambda cc: cc.value, CodeChannel))
