from __future__ import annotations

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
        # Actual IPv4 address of the network adapter or null if unknown
        self._actual_IP = ""
        # Configured IPv4 address of the network adapter or null if unknown
        self._configured_IP = ""
        # Configured IPv4 DNS server fo the network adapter or null if unknown
        self._dns_server = ""
        # Version of the network interface or None if unknown.
        self._firmware_version = ""
        # IPv4 gateway of the network adapter or null if unknown
        self._gateway = ""
        # Physical address of the network adapter or null if unknown
        self._mac = ""
        # Number of reconnect attempts or None if unknown
        self._num_reconnects = None
        # Signal of the Wi-Fi adapter (only Wi-Fi, in dBm, or None if unknown)
        self._signal = None
        # Speed of the network interface (in MBit, None if unknown, 0 if not connected)
        self._speed = None
        # SSID of the Wi-Fi network or null if not applicable
        self._ssid = None
        # State of this network interface or null if unknown
        self._state = None
        # Subnet of the network adapter or null if unknown
        self._subnet = None
        # Type of this network interface
        self._type = NetworkInterfaceType.wifi
        # WiFi country code if this is a WiFi adapter and if the country code can be determined
        self._wifi_country = None

    @property
    def active_protocols(self) -> list[NetworkProtocol]:
        """List of active protocols"""
        return self._active_protocols

    @property
    def actual_IP(self) -> Union[str, None]:
        """Actual IPv4 address of the network adapter or null if unknown"""
        return self._actual_IP
    
    @actual_IP.setter
    def actual_IP(self, value: str | None = None):
        self._actual_IP = str(value) if value is not None else None
        
    @property
    def configured_IP(self) -> Union[str, None]:
        """Configured IPv4 address of the network adapter or null if unknown"""
        return self._configured_IP
    
    @configured_IP.setter
    def configured_IP(self, value: str | None = None):
        self._configured_IP = str(value) if value is not None else None
        
    @property
    def dns_server(self) -> Union[str, None]:
        """Configured IPv4 DNS server fo the network adapter or null if unknown"""
        return self._dns_server
    
    @dns_server.setter
    def dns_server(self, value: str | None = None):
        self._dns_server = str(value) if value is not None else None
        
    @property
    def firmware_version(self) -> str | None:
        """Version of the network interface or None if unknown."""
        return self._firmware_version
    
    @firmware_version.setter
    def firmware_version(self, value: str | None = None):
        self._firmware_version = str(value) if value is not None else None
        
    @property
    def gateway(self) -> Union[str, None]:
        """IPv4 gateway of the network adapter or null if unknown"""
        return self._gateway
    
    @gateway.setter
    def gateway(self, value: str | None = None):
        self._gateway = str(value) if value is not None else None
    
    @property
    def mac(self) -> Union[str, None]:
        """Physical address of the network adapter or null if unknown"""
        return self._mac
    
    @mac.setter
    def mac(self, value: str | None = None):
        self._mac = str(value) if value is not None else None
        
    @property
    def num_reconnects(self) -> int | None:
        """Number of reconnect attempts or None if unknown"""
        return self._num_reconnects
    
    @num_reconnects.setter
    def num_reconnects(self, value: int | None = None):
        self._num_reconnects = int(value) if value is not None else None
        
    @property
    def signal(self) -> int | None:
        """Signal of the Wi-Fi adapter (only Wi-Fi, in dBm, or None if unknown)"""
        return self._signal
    
    @signal.setter
    def signal(self, value: int | None = None):
        self._signal = int(value) if value is not None else None

    @property
    def speed(self) -> int | None:
        """Speed of the network interface (in MBit, None if unknown, 0 if not connected)"""
        return self._speed

    @speed.setter
    def speed(self, value: int | None = None):
        self._speed = int(value) if value is not None else None

    @property
    def ssid(self) -> Union[str, None]:
        """SSID of the Wi-Fi network or null if not applicable"""
        return self._ssid

    @ssid.setter
    def ssid(self, value):
        self._ssid = str(value) if value is not None else None
    
    @property
    def state(self) -> Union[NetworkState, None]:
        """State of this network interface or null if unknown"""
        return self._state
    
    @state.setter
    def state(self, value: NetworkState | None = None):
        if value is None or isinstance(value, NetworkState):
            self._state = value
        elif isinstance(value, str):
            self._state = NetworkState(value)
        else:
            raise TypeError(f"{__name__}.state must be of type NetworkState or None."
                            f" Got {type(value)}: {value}")
        
    @property
    def subnet(self) -> Union[str, None]:
        """Subnet of the network adapter or null if unknown"""
        return self._subnet
    
    @subnet.setter
    def subnet(self, value: str | None = None):
        self._subnet = str(value) if value is not None else None
        
    @property
    def type(self) -> NetworkInterfaceType:
        """Type of this network interface"""
        return self._type
    
    @type.setter
    def type(self, value: NetworkInterfaceType = NetworkInterfaceType.wifi):
        if isinstance(value, NetworkInterfaceType):
            self._type = value
        elif isinstance(value, str):
            self._type = NetworkInterfaceType(value)
        else:
            raise TypeError(f"{__name__}.type must be of type NetworkInterfaceType. Got {type(value)}: {value}")

    @property
    def wifi_country(self) -> Union[str, None]:
        """WiFi country code if this is a WiFi adapter and if the country code can be determined
        For this setting to be populated in SBC mode it is required to have the DuetPiManagementPlugin running.
        This is required due to missing Linux permissions of the control server."""
        return self._wifi_country

    @wifi_country.setter
    def wifi_country(self, value):
        self._wifi_country = None if value is None else str(value)
