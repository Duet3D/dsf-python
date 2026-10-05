from enum import Enum

from ...utils import DeprecatedAliasEnumType


class NetworkInterfaceType(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Supported types of network interfaces"""

    # Wired network interface
    ETHERNET = "ethernet"

    # Wireless network interface
    WIFI = "wifi"

    # Previous names, deprecated
    ethernet = ETHERNET
    wifi = WIFI
