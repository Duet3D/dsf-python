from enum import Enum


class CommunicationMethod(str, Enum):
    """Supported communication methods"""

    # SPI link adapter
    SPI = "spi"

    # USB link adapter
    USB = "usb"