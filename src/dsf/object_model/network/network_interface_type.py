from enum import Enum


class NetworkInterfaceType(str, Enum):
    """Supported types of network interfaces"""

    # Wired network interface
    ethernet = "ethernet"

    # Wireless network interface
    wifi = "wifi"
