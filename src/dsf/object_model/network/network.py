from .network_interface import NetworkInterface
from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import model_prop, nullable_model_prop


class Network(ModelObject):
    """Information about the network subsystem"""

    # Default name of the machine
    DEFAULT_NAME = "My Duet"
    # Fallback hostname if the <c>Name</c> is invalid
    DEFAULT_HOSTNAME = "duet"
    # Default network password of the machine
    DEFAULT_PASSWORD = "reprap"

    # If this is set, the web server will allow cross-origin requests via the Access-Control-Allow-Origin header
    cors_site = nullable_model_prop("cors_site", str)

    # Hostname of the machine
    hostname = model_prop("hostname", str, DEFAULT_HOSTNAME)

    # List of available network interfaces
    interfaces = model_prop("interfaces", ModelCollection[NetworkInterface], ModelCollection(NetworkInterface))

    # Name of the machine
    name = model_prop("name", str, DEFAULT_NAME)

    def __init__(self):
        super().__init__()
