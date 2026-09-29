__version__ = "3.7.0-beta.1"

import json
import os


def _read_socket_file(config_path: str = "/opt/dsf/conf/config.json") -> str:
    """Read the socket file path from the DSF config, falling back to the default path"""
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                socket_dir: str = config.get("SocketDirectory", "/run/dsf")
                socket_file: str = config.get("SocketFile", "dcs.sock")
                return os.path.join(socket_dir, socket_file)
        except (json.JSONDecodeError, IOError):
            pass  # Use default if config file is invalid or inaccessible
    return "/run/dsf/dcs.sock"


# Socket file path
SOCKET_FILE = _read_socket_file()

# allowed connection per unix server
DEFAULT_BACKLOG = 4

# DSF protocol version
PROTOCOL_VERSION = 13

from . import commands, connections, http, object_model


__all__ = ['SOCKET_FILE', 'DEFAULT_BACKLOG', 'PROTOCOL_VERSION', 'commands', 'connections', 'http', 'object_model']
