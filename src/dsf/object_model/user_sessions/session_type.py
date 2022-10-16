from enum import Enum


class SessionType(str, Enum):
    """Types of user sessions"""

    # Local client
    local = "local"

    # Remote client via HTTP
    http = "http"

    # Remote client via Telnet
    telnet = "telnet"
