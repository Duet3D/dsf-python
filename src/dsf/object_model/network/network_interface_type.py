from enum import Enum


class NetworkInterfaceType(str, Enum):
    """Supported types of network interfaces"""

    # Wired network interface
    lan = "lan"

    # Wireless network interface
    wifi = "wifi"
