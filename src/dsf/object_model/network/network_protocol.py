from enum import Enum


class NetworkProtocol(str, Enum):
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
    Telnet = "telnet"

    # SSH protocol
    SSH = "ssh"
