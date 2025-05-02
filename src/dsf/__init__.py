__version__ = "3.6.0-rc.3"

import json
import os

# Default socket file path
SOCKET_FILE = "/run/dsf/dcs.sock"

# Try to read socket file path from config
config_path = "/opt/dsf/conf/config.json"
if os.path.exists(config_path):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            socket_dir = config.get("SocketDirectory", "/run/dsf")
            socket_file = config.get("SocketFile", "dcs.sock")
            SOCKET_FILE = os.path.join(socket_dir, socket_file)
    except (json.JSONDecodeError, IOError):
        pass  # Use default if config file is invalid or inaccessible

# allowed connection per unix server
DEFAULT_BACKLOG = 4

# DSF protocol version
PROTOCOL_VERSION = 12

from . import commands, connections, http, object_model
