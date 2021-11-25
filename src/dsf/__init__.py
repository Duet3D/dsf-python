# path to unix socket file
SOCKET_FILE = "/run/dsf/dcs.sock"

# allowed connection per unix server
DEFAULT_BACKLOG = 4

# DSF protocol version
PROTOCOL_VERSION = 11

from . import commands, connections, http, initmessages, models
