from typing import Optional

from .base_command import BaseCommand


def get_object_model(filters: list[str] = []):
    """
    Query the current object model.
    :param filters: Optional object model key paths to retrieve.
                    If any key paths are given, the returned instance holds only the requested parts and every other
                    property is left at its default value. There is no way to tell those apart from values that are
                    genuinely unset.
    """
    return BaseCommand("GetObjectModel", **{"filters": filters})


def patch_object_model(key: str, patch: str):
    """
    Apply a full patch to the object model. May be used only in non-SPI mode
    :param key: Key to update
    :param patch: JSON patch to apply
    """
    return BaseCommand("PatchObjectModel", **{"key": key, "patch": patch})


def query_object_model(key: str = "", flags: str = ""):
    """
    Query the object model using a key and flags, returning a formatted JSON response
    compatible with the M409 response format without going through the code execution pipeline
    :param key: Object model key path to query (e.g. "heat", "move.axes", "" for root)
    :param flags: RRF-compatible flags string controlling response content:
                  'f' = only include live (frequently changing) properties,
                  'n' = include null values,
                  'v' = include verbose properties,
                  'o' = include obsolete properties,
                  'a' followed by digits = array start index,
                  'd' followed by digits = max depth
    """
    return BaseCommand("QueryObjectModel", **{"key": key, "flags": flags})


def set_network_protocol(protocol: str, enabled: bool):
    """Flag a given network protocol as enabled or disabled
    :param protocol: Protocol to change
    :param enabled: Whether the protocol is enabled or not
    :returns: true if the protocol could be flagged
    """
    return BaseCommand("SetNetworkProtocol", **{"protocol": protocol, "enabled": enabled})


def sync_object_model():
    """Wait for the machine model to be fully updated from RepRapFirmware."""
    return BaseCommand("SyncObjectModel")


def set_wifi_country(country_code: Optional[str] = None):
    """
    Set the WiFi country code. This is a global setting on Linux, so it is applied to every WiFi interface
    in the object model
    :param country_code: New WiFi country code, or null to clear it
    """
    return BaseCommand("SetWifiCountry", **{"countryCode": country_code})
