from enum import Enum

from .....utils import DeprecatedAliasEnumType


class SessionType(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Types of user sessions"""

    # Local client
    LOCAL = "local"

    # Remote client via HTTP
    HTTP = "http"

    # Remote client via Telnet
    TELNET = "telnet"

    # Previous names, deprecated
    http = HTTP
    local = LOCAL
    telnet = TELNET
