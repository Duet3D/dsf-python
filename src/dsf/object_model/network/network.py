from __future__ import annotations

from .network_interface import NetworkInterface
from ..model_collection import ModelCollection
from ..model_object import ModelObject


class Network(ModelObject):
    """Information about the network subsystem"""

    # Default name of the machine
    DEFAULT_NAME = "My Duet"
    # Fallback hostname if the <c>Name</c> is invalid
    DEFAULT_HOSTNAME = "duet"
    # Default network password of the machine
    DEFAULT_PASSWORD = "reprap"

    def __init__(self):
        super().__init__()
        # If this is set, the web server will allow cross-origin requests via the Access-Control-Allow-Origin header
        self._cors_site = ""
        # Hostname of the machine
        self._hostname = Network.DEFAULT_HOSTNAME
        # List of available network interfaces
        self._interfaces = ModelCollection(NetworkInterface)
        # Name of the machine
        self._name = Network.DEFAULT_NAME

    @property
    def cors_site(self) -> str | None:
        """If this is set, the web server will allow cross-origin requests via the Access-Control-Allow-Origin header"""
        return self._cors_site

    @cors_site.setter
    def cors_site(self, value: str | None = None):
        self._cors_site = str(value) if value is not None else None

    @property
    def hostname(self) -> str | None:
        """Hostname of the machine"""
        return self._hostname

    @hostname.setter
    def hostname(self, value: str | None = None):
        self._hostname = str(value) if value is not None else None

    @property
    def interfaces(self) -> list[NetworkInterface]:
        """List of available network interfaces"""
        return self._interfaces

    @property
    def name(self) -> str | None:
        """Name of the machine"""
        return self._name

    @name.setter
    def name(self, value: str | None = None):
        self._name = str(value) if value is not None else None
