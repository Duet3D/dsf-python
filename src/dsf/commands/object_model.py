from .base_command import BaseCommand


def get_object_model():
    """Query the current object model."""
    return BaseCommand("GetObjectModel")


def lock_object_model():
    """
    Lock the object model for read/write access.
    This may be used to update the machine model and to change array items.
    """
    return BaseCommand("LockObjectModel")


def patch_object_model(key: str, patch: str):
    """
    Apply a full patch to the object model. May be used only in non-SPI mode
    :param key: Key to update
    :param patch: JSON patch to apply
    """
    if not isinstance(key, str) or not key:
        raise TypeError("key must be a string")
    if not isinstance(patch, str) or not patch:
        raise TypeError("patch must be a string")
    return BaseCommand("PatchObjectModel", **{"Key": key, "Patch": patch})


def set_network_protocol(protocol: str, enabled: bool):
    """Flag a given network protocol as enabled or disabled
    The object model must not be locked from the same connection via lock_object_model when this is called!
    :param protocol: Protocol to change
    :param enabled: Whether the protocol is enabled or not
    :returns: true if the protocol could be flagged
    """
    if not isinstance(protocol, str) or not protocol:
        raise TypeError("protocol must be a string")
    if not isinstance(enabled, bool):
        raise TypeError("enabled must be a boolean")
    return BaseCommand("SetNetworkProtocol", **{"NetworkProtocol": protocol, "Enabled": enabled})


def set_object_model(property_path: str, value: str):
    """
    Set an atomic property in the object model.
    Make sure to acquire the read/write lock first!
    :param property_path: Path to the property in the machine model
    :param value: String representation of the value to set
    :returns: true if the field could be updated
    """
    if not isinstance(property_path, str) or not property_path:
        raise TypeError("property_path must be a string")
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    return BaseCommand("SetObjectModel", **{"PropertyPath": property_path, "Value": value})


def sync_object_model():
    """Wait for the machine model to be fully updated from RepRapFirmware."""
    return BaseCommand("SyncObjectModel")


def unlock_object_model():
    """
    Unlock the machine model after obtaining read/write access.
    This is mandatory after LockObjectModel has been invoked.
    """
    return BaseCommand("UnlockObjectModel")
