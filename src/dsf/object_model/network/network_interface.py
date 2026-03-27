from typing import List, Union

from .network_interface_type import NetworkInterfaceType
from .network_protocol import NetworkProtocol
from .network_state import NetworkState
from ..model_object import ModelObject
from ..model_collection import ModelCollection
from ..utils import nullable_model_prop, model_prop
from ...utils import deprecated


class NetworkInterface(ModelObject):
    """Information about a network interface"""

    # List of active protocols
    active_protocols = model_prop('active_protocols', ModelCollection[NetworkProtocol], ModelCollection(NetworkProtocol))

    # Actual IPv4 address of the network adapter or null if unknown
    actual_IP = nullable_model_prop('actual_IP', str)
    
    # Configured IPv4 address of the network adapter or null if unknown
    configured_IP = nullable_model_prop('configured_IP', str)
    
    # Configured IPv4 DNS server fo the network adapter or null if unknown
    dns_server = nullable_model_prop('dns_server', str)
    
    firmware_version = nullable_model_prop('firmware_version', str)

    # IPv4 gateway of the network adapter or null if unknown
    gateway = nullable_model_prop('gateway', str)

    # Physical address of the network adapter or null if unknown
    mac = nullable_model_prop('mac', str)

    # Number of reconnect attempts or null if unknown
    # This is only reported by ESP-base boards in standalone mode
    num_reconnects = nullable_model_prop('num_reconnects', int)

    # Received signal strength indicator of the WiFi adapter (only WiFi, in dBm, or null if unknown)
    rssi = nullable_model_prop('rssi', int)

    # Speed of the network interface (in MBit, null if unknown, 0 if not connected)
    speed = nullable_model_prop('speed', int)

    # SSID of the Wi-Fi network or null if not applicable
    ssid = nullable_model_prop('ssid', str)

    # State of this network interface or null if unknown
    state = nullable_model_prop('state', NetworkState, constructor=lambda: None)

    # Subnet of the network adapter or null if unknown
    subnet = nullable_model_prop('subnet', str)

    # Type of this network interface
    type = model_prop('type', NetworkInterfaceType, NetworkInterfaceType.wifi)

    # WiFi country code if this is a WiFi adapter and if the country code can be determined
    wifi_country = nullable_model_prop('wifi_country', str)

    def __init__(self):
        super().__init__()
