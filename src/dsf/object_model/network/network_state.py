from enum import Enum

from ...utils import DeprecatedAliasEnumType


class NetworkState(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Enumeration of possible network interface states"""

    # Network disabled
    DISABLED = "disabled"

    # Network enabled but not started yet
    ENABLED = "enabled"

    # Tried to start the network but initialisation failed
    INIT_FAILED = "initFailed"

    # Starting up (used by Wi-Fi networking in standalone mode)
    STARTING1 = "starting1"

    # Starting up (used by Wi-Fi networking in standalone mode)
    STARTING2 = "starting2"

    # Running and in the process of switching between modes (used by Wi-Fi networking in standalone mode)
    CHANGING_MODE = "changingMode"

    # Starting up, waiting for link
    ESTABLISHING_LINK = "establishingLink"

    # Link established, waiting for DHCP
    OBTAINING_IP = "obtainingIP"

    # Just established a connection
    CONNECTED = "connected"

    # Network running
    ACTIVE = "active"

    # WiFi adapter is idle
    IDLE = "idle"

    # Previous names, deprecated
    active = ACTIVE
    changingMode = CHANGING_MODE
    connected = CONNECTED
    disabled = DISABLED
    enabled = ENABLED
    establishingLink = ESTABLISHING_LINK
    idle = IDLE
    initFailed = INIT_FAILED
    obtainingIP = OBTAINING_IP
    starting1 = STARTING1
    starting2 = STARTING2
