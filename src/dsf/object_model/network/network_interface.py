from typing import List, Union

from .network_interface_type import NetworkInterfaceType
from .network_protocol import NetworkProtocol
from .network_state import NetworkState
from ..model_object import ModelObject


class NetworkInterface(ModelObject):
    """Information about a network interface"""

    def __init__(self):
        super().__init__()
        # List of active protocols
        self._active_protocols = []
        # Actual IPv4 address of the network adapter
        self._actual_IP = ""
        # Configured IPv4 address of the network adapter
        self._configured_IP = ""
        # Configured IPv4 DNS server fo the network adapter
        self._dns_server = ""
        # Version of the network interface or null if unknown.
        self._firmware_version = ""
        # IPv4 gateway of the network adapter
        self._gateway = ""
        # Physical address of the network adapter
        self._mac = ""
        # Number of reconnect attempts or null if unknown
        self._num_reconnects = None
        # Signal of the Wi-Fi adapter (only Wi-Fi, in dBm, or null if unknown)
        self._signal = None
        # Speed of the network interface (in MBit, null if unknown, 0 if not connected)
        self._speed = None
        # Network state
        self._state = None
        # Subnet of the network adapter
        self._subnet = None
        # Type of this network interface
        self._type = NetworkInterfaceType.wifi

    @property
    def active_protocols(self) -> List[NetworkProtocol]:
        """List of active protocols"""
        return self._active_protocols

    @property
    def actual_IP(self) -> Union[str, None]:
        """Actual IPv4 address of the network adapter"""
        return self._actual_IP
    
    @actual_IP.setter
    def actual_IP(self, value):
        self._actual_IP = str(value) if value is not None else None
        
    @property
    def configured_IP(self) -> Union[str, None]:
        """Configured IPv4 address of the network adapter"""
        return self._configured_IP
    
    @configured_IP.setter
    def configured_IP(self, value):
        self._configured_IP = str(value) if value is not None else None
        
    @property
    def dns_server(self) -> Union[str, None]:
        """Configured IPv4 DNS server fo the network adapter"""
        return self._dns_server
    
    @dns_server.setter
    def dns_server(self, value):
        self._dns_server = str(value) if value is not None else None
        
    @property
    def firmware_version(self) -> Union[str, None]:
        """Version of the network interface or null if unknown.
        This is primarily intended for the ESP8266-based network interfaces as used on the Duet WiFi"""
        return self._firmware_version
    
    @firmware_version.setter
    def firmware_version(self, value):
        self._firmware_version = str(value) if value is not None else None
        
    @property
    def gateway(self) -> Union[str, None]:
        """IPv4 gateway of the network adapter"""
        return self._gateway
    
    @gateway.setter
    def gateway(self, value):
        self._gateway = str(value) if value is not None else None
    
    @property
    def mac(self) -> Union[str, None]:
        """Physical address of the network adapter"""
        return self._mac
    
    @mac.setter
    def mac(self, value):
        self._mac = str(value) if value is not None else None
        
    @property
    def num_reconnects(self) -> Union[int, None]:
        """Number of reconnect attempts or null if unknown"""
        return self._num_reconnects
    
    @num_reconnects.setter
    def num_reconnects(self, value):
        self._num_reconnects = int(value) if value is not None else None
        
    @property
    def signal(self) -> Union[int, None]:
        """Signal of the Wi-Fi adapter (only Wi-Fi, in dBm, or null if unknown)"""
        return self._signal
    
    @signal.setter
    def signal(self, value):
        self._signal = int(value) if value is not None else None
        
    @property
    def speed(self) -> Union[int, None]:
        """Speed of the network interface (in MBit, null if unknown, 0 if not connected)"""
        return self._speed
    
    @speed.setter
    def speed(self, value):
        self._speed = int(value) if value is not None else None
    
    @property
    def state(self) -> Union[NetworkState, None]:
        """Network state"""
        return self._state
    
    @state.setter
    def state(self, value):
        if value is None or isinstance(value, NetworkState):
            self._state = value
        elif isinstance(value, str):
            self._state = NetworkState(value)
        else:
            raise TypeError(f"{__name__}.state must be of type NetworkState. Got {type(value)}: {value}")
        
    @property
    def subnet(self) -> Union[str, None]:
        """Subnet of the network adapter"""
        return self._subnet
    
    @subnet.setter
    def subnet(self, value):
        self._subnet = str(value) if value is not None else None
        
    @property
    def type(self) -> NetworkInterfaceType:
        """Type of this network interface"""
        return self._type
    
    @type.setter
    def type(self, value):
        if value is None or value == "":
            self._type = NetworkInterfaceType.wifi
        elif isinstance(value, NetworkInterfaceType):
            self._type = value
        elif isinstance(value, str):
            self._type = NetworkInterfaceType(value)
        else:
            raise TypeError(f"{__name__}.type must be of type NetworkInterfaceType. Got {type(value)}: {value}")

    def _update_from_json(self, **kwargs) -> 'NetworkInterface':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(NetworkInterface, self)._update_from_json(**kwargs)
        self._active_protocols = [NetworkProtocol(item) for item in kwargs.get('activeProtocols', [])]
        return self
