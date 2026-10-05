from enum import Enum

from ...utils import DeprecatedAliasEnumType


class NetworkProtocol(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Supported network protocols"""

    # HTTP protocol
    HTTP = "http"

    # HTTPS protocol
    HTTPS = "https"

    # FTP protocol
    FTP = "ftp"

    # SFTP protocol
    SFTP = "sftp"

    # Telnet protocol
    TELNET = "telnet"

    # SSH protocol
    SSH = "ssh"

    # Previous names, deprecated
    Telnet = TELNET
