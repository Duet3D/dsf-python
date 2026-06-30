from enum import Enum


class CommunicationMethod(str, Enum):
    """Supported communication methods"""

    # SPI link adapter
    SPI = "SPI"

    # USB link adapter
    USB = "USB"