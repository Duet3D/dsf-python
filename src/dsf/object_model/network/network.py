from typing import List, Union

from .network_interface import NetworkInterface
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
        self._interfaces = []
        # Name of the machine
        self._name = Network.DEFAULT_NAME

    @property
    def cors_site(self) -> Union[str, None]:
        """If this is set, the web server will allow cross-origin requests via the Access-Control-Allow-Origin header"""
        return self._cors_site

    @cors_site.setter
    def cors_site(self, value):
        self._cors_site = str(value) if value is not None else None

    @property
    def hostname(self) -> Union[str, None]:
        """Hostname of the machine"""
        return self._hostname

    @hostname.setter
    def hostname(self, value):
        self._hostname = str(value) if value is not None else None

    @property
    def interfaces(self) -> List[NetworkInterface]:
        """List of available network interfaces"""
        return self._interfaces

    @property
    def name(self) -> Union[str, None]:
        """Name of the machine"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value) if value is not None else None

    def _update_from_json(self, **kwargs) -> 'Network':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(Network, self)._update_from_json(**kwargs)
        self._interfaces = [NetworkInterface.from_json(i) for i in kwargs.get('interfaces', [])]
        return self
