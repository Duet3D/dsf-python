from enum import Enum


class NetworkState(str, Enum):
    """Enumeration of possible network interface states"""

    # Network disabled
    disabled = "disabled"

    # Network enabled but not started yet
    enabled = "enabled"

    # Starting up (used by Wi-Fi networking in standalone mode)
    starting1 = "starting1"

    # Starting up (used by Wi-Fi networking in standalone mode)
    starting2 = "starting2"

    # Running and in the process of switching between modes (used by Wi-Fi networking in standalone mode)
    changingMode = "changingMode"

    # Starting up, waiting for link
    establishingLink = "establishingLink"

    # Link established, waiting for DHCP
    obtainingIP = "obtainingIP"

    # Just established a connection
    connected = "connected"

    # Network running
    active = "active"
