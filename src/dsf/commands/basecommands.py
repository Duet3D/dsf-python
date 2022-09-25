"""
This module contains all basic commands to be sent to the server.

    Python interface to DuetSoftwareFramework
    Copyright (C) 2020 Duet3D

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from enum import IntEnum, Enum
from typing import Optional
from warnings import warn

from .codechannel import CodeChannel


DEPRECATED_NAMES = [
    ("get_machine_model", "get_object_model"),
    ("sync_machine_model", "sync_object_model"),
    ("lock_machine_model", "lock_object_model"),
    ("unlock_machine_model", "unlock_object_model")
]


def __getattr__(name):
    for old_name, new_name in DEPRECATED_NAMES:
        if name == old_name:
            msg = f"{name} is deprecated and is going to be removed in the next release."
            if len(new_name):
                msg += f" Please use {new_name} instead."
            warn(msg, FutureWarning, stacklevel=2)
            return globals()[f"_deprecated_{name}"]
    raise AttributeError(f"module {__name__} has no attribute {name}")


class HttpEndpointType(str, Enum):
    """Enumeration of supported HTTP request types"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    TRACE = "TRACE"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    WebSocket = "WebSocket"


class AccessLevel(str, Enum):
    """Defines what a user is allowed to do"""

    ReadOnly = "ReadOnly"
    ReadWrite = "ReadWrite"


class SessionType(str, Enum):
    """Types of user sessions"""

    Local = "Local"
    HTTP = "HTTP"
    Telnet = "Telnet"


class MessageType(IntEnum):
    """Type of Resolve message"""

    Success = 0
    Warning = 1
    Error = 2


class LogLevel(str, Enum):
    """Configured log level"""

    Debug = "debug"
    Info = "info"
    Warn = "warn"
    Off = "off"


class BaseCommand:
    """Base class of a command."""

    @classmethod
    def from_json(cls, data):
        """Deserialize an instance of this class from a JSON deserialized dictionary"""
        return cls(**data)

    def __init__(self, command: str, **kwargs):
        self.command = command
        for key, value in kwargs.items():
            self.__dict__[key] = value


def acknowledge():
    """
    Acknowledge a (partial) model update.
    This command is only permitted in ConnectionMode.Subscribe mode.
    """
    return BaseCommand("Acknowledge")


def cancel():
    """Cancel a code in Connection.InterceptionMode."""
    return BaseCommand("Cancel")


def ignore():
    """
    Ignore the code to intercept and allow it to be processed without any modifications.
    This command is only permitted in ConnectionMode.Intercept mode.
    """
    return BaseCommand("Ignore")


def _deprecated_get_machine_model():
    return BaseCommand("GetObjectModel")


def get_object_model():
    """Query the current object model."""
    return BaseCommand("GetObjectModel")


def _deprecated_sync_machine_model():
    return BaseCommand("SyncObjectModel")


def sync_object_model():
    """Wait for the machine model to be fully updated from RepRapFirmware."""
    return BaseCommand("SyncObjectModel")


def _deprecated_lock_machine_model():
    return BaseCommand("LockObjectModel")


def lock_object_model():
    """
    Lock the object model for read/write access.
    This may be used to update the machine model and to change array items.
    """
    return BaseCommand("LockObjectModel")


def _deprecated_unlock_machine_model():
    return BaseCommand("UnlockObjectModel")


def unlock_object_model():
    """
    Unlock the machine model after obtaining read/write access.
    This is mandatory after LockObjectModel has been invoked.
    """
    return BaseCommand("UnlockObjectModel")


def add_http_endpoint(
    endpoint_type: HttpEndpointType, namespace: str, path: str, is_upload_request: bool
):
    """
    Register a new HTTP endpoint via DuetWebServer.
    This will create a new HTTP endpoint under /machine/{Namespace}/{EndpointPath}.
    :param endpoint_type: Type of the HTTP request
    :param namespace: Namespace of the plugin wanting to create a new third-party endpoint
    :param path: Path to the endpoint to register
    :param is_upload_request: Whether this is an upload request
    :returns: a path to the UNIX socket which DuetWebServer will connect
    to whenever a matching HTTP request is received.
    A plugin using this command has to open a new UNIX socket with the given path that DuetWebServer can connect to
    """
    if not isinstance(endpoint_type, HttpEndpointType):
        raise TypeError("endpoint_type must be a HttpEndpointType")
    if not isinstance(namespace, str) or not namespace:
        raise TypeError("namespace must be a string")
    if not isinstance(path, str) or not path:
        raise TypeError("path must be a string")
    if not isinstance(is_upload_request, bool):
        raise TypeError("is_upload_request must be a boolean")
    return BaseCommand(
        "AddHttpEndpoint",
        **{
            "EndpointType": endpoint_type,
            "Namespace": namespace,
            "Path": path,
            "IsUploadRequest": is_upload_request,
        },
    )


def remove_http_endpoint(endpoint_type: HttpEndpointType, namespace: str, path: str):
    """
    Remove an existing HTTP endpoint.
    :param endpoint_type: Type of the endpoint
    :param namespace: Namespace of the endpoint
    :param path: Path to the endpoint to unregister
    :returns: true if the endpoint could be successfully removed
    """
    if not isinstance(endpoint_type, HttpEndpointType):
        raise TypeError("endpoint_type must be a HttpEndpointType")
    if not isinstance(namespace, str) or not namespace:
        raise TypeError("namespace must be a string")
    if not isinstance(path, str) or not path:
        raise TypeError("path must be a string")
    return BaseCommand(
        "RemoveHttpEndpoint",
        **{"EndpointType": endpoint_type, "Namespace": namespace, "Path": path},
    )


def check_password(password: str):
    """
    Check if the given password is correct and matches the previously set value from M551.
    If no password was configured before or if it was set to "reprap", this will always return true
    :param password: Password to check
    :returns: true if the password matches or is not set
    """
    if not isinstance(password, str) or not password:
        raise TypeError("password must be a string")
    return BaseCommand("CheckPassword", **{"Password": password})


def add_user_session(
    access: AccessLevel, tpe: SessionType, origin: str, origin_port: int
):
    """
    Register a new user session.
    Returns the ID of the new user session
    :param access: Access level of this session
    :param tpe: Type of this session
    :param origin: Origin of this session. For remote sessions, this equals the remote IP address
    """
    if not isinstance(access, AccessLevel):
        raise TypeError("access must be an AccessLevel")
    if not isinstance(tpe, SessionType):
        raise TypeError("tpe must be an SessionType")
    if not isinstance(origin, str) or not origin:
        raise TypeError("origin must be a string")
    if not isinstance(origin_port, int):
        raise TypeError("origin_port must be an int")
    return BaseCommand(
        "AddUserSession",
        **{
            "AccessLevel": access,
            "SessionType": tpe,
            "Origin": origin,
            "OriginPort": origin_port,
        },
    )


def remove_user_session(session_id: int):
    """
    Remove an existing user session
    :param session_id: Identifier of the user session to remove
    """
    if not isinstance(session_id, int):
        raise TypeError("session_id must be an int")
    return BaseCommand("RemoveUserSession", **{"Id": session_id})


def evaluate_expression(channel: CodeChannel, expression: str):
    """
    Evaluate an arbitrary expression on the given channel in RepRapFirmware.
    Do not use this call to evaluate file-based and network-related fields because the
    DSF and RRF models diverge in this regard.
    :param channel: Code channel where the expression is evaluated
    :param expression: Expression to evaluate
    """
    if not isinstance(channel, CodeChannel):
        raise TypeError("channel must be a CodeChannel")
    if not isinstance(expression, str) or not expression:
        raise TypeError("expression must be a string")
    return BaseCommand(
        "EvaluateExpression", **{"Channel": channel, "Expression": expression}
    )


def flush(channel: CodeChannel):
    """
    Wait for all pending (macro) codes on the given channel to finish.
    This effectively guarantees that all buffered codes are processed by RRF before this command finishes.
    :param channel: Code channel to flush
    :returns: true if the flush request is successful
    """
    if not isinstance(channel, CodeChannel):
        raise TypeError("channel must be a CodeChannel")
    return BaseCommand("Flush", **{"Channel": channel})


def get_file_info(file_name: str):
    """
    Analyse a G-code file and return an instance of GetFileInfo when ready
    :param file_name: The filename to extract information from
    """
    if not isinstance(file_name, str) or not file_name:
        raise TypeError("file_name must be a string")
    return BaseCommand("GetFileInfo", **{"FileName": file_name})


def resolve_path(path: str):
    """
    Resolve a RepRapFirmware-style path to an actual file path
    :param path: Path that is RepRapFirmware-compatible
    :returns: The resolved path
    """
    if not isinstance(path, str) or not path:
        raise TypeError("path must be a string")
    return BaseCommand("ResolvePath", **{"Path": path})


def simple_code(code: str, channel: CodeChannel):
    """
    Perform a simple G/M/T-code
    Internally the code passed is populated as a full Code instance and on completion
    its Code.Result is transformed back into a basic string. This is useful for minimal
    extensions that do not require granular control of the code details. Except for certain cases, it
    is NOT recommended for usage in InterceptionMode because it renders the internal code buffer useless.
    :param code: Code to parse and execute
    :param channel: Destination channel
    """
    if not isinstance(code, str) or not code:
        raise TypeError("code must be a string")
    if not isinstance(channel, CodeChannel):
        raise TypeError("channel must be a CodeChannel")
    return BaseCommand("SimpleCode", **{"Code": code, "Channel": channel})


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
    return BaseCommand(
        "SetObjectModel", **{"PropertyPath": property_path, "Value": value}
    )


def set_update_status(updating: bool):
    """
    Override the current status as reported by the object model when performing a software update.
    :param updating: Whether an update is now in progress
    """
    if not isinstance(updating, bool):
        raise TypeError("updating must be a bool")
    return BaseCommand("SetUpdateStatus", **{"Updating": updating})


def install_plugin(plugin_file: str):
    """
    Install or upgrade a plugin
    :param plugin_file: Absolute file path to the plugin ZIP bundle
    """
    if not isinstance(plugin_file, str) or not plugin_file:
        raise TypeError("plugin_file must be a string")
    return BaseCommand("InstallPlugin", **{"PluginFile": plugin_file})


def set_plugin_data(plugin: str, key: str, value: str):
    """
    Update custom plugin data in the object model
    May be used to update only the own plugin data unless the plugin has the ManagePlugins permission.
    Note that the corresponding key must already exist in the plugin data!
    :param plugin: Identifier of the plugin to update (only mandatory if running as root)
    :param key: Key to set. This key must already exist in the ObjectModel.PluginManifest.Data object!
    :param value: Custom value to set
    """
    if not isinstance(plugin, str) or not plugin:
        raise TypeError("plugin must be a string")
    if not isinstance(key, str) or not key:
        raise TypeError("key must be a string")
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    return BaseCommand(
        "SetPluginData", **{"Plugin": plugin, "Key": key, "Value": value}
    )


def start_plugin(plugin: str):
    """
    Start a plugin
    :param plugin: Identifier of the plugin
    """
    if not isinstance(plugin, str) or not plugin:
        raise TypeError("plugin must be a string")
    return BaseCommand("StartPlugin", **{"Plugin": plugin})


def stop_plugin(plugin: str):
    """
    Stop a plugin
    :param plugin: Identifier of the plugin
    """
    if not isinstance(plugin, str) or not plugin:
        raise TypeError("plugin must be a string")
    return BaseCommand("StopPlugin", **{"Plugin": plugin})


def uninstall_plugin(plugin: str):
    """
    Uninstall a plugin
    :param plugin: Identifier of the plugin
    """
    if not isinstance(plugin, str) or not plugin:
        raise TypeError("plugin must be a string")
    return BaseCommand("UninstallPlugin", **{"Plugin": plugin})


def write_message(
    message_type: MessageType,
    content: str,
    output_message: bool,
    log_level: Optional[LogLevel],
):
    """
    Write an arbitrary generic message
    :param message_type: Type of the message to write
    :param content: Content of the message to write
    :param output_message: Output the message on the console and via the object model
    :param log_level: Log level of this message
    """
    if not isinstance(message_type, MessageType):
        raise TypeError("rtype must be a MessageType")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(output_message, bool):
        raise TypeError("output_message must be a bool")
    if log_level is not None and not isinstance(log_level, LogLevel):
        raise TypeError("log_message must be a LogLevel")
    return BaseCommand(
        "WriteMessage",
        **{
            "Type": message_type,
            "Content": content,
            "OutputMessage": output_message,
            "LogLevel": log_level,
        },
    )


def resolve_code(rtype: MessageType, content: Optional[str]):
    """
    Resolve the code to intercept and return the given message details for its completion.
    This command is only permitted in ConnectionMode.Intercept mode.
    :param rtype: Type of the resolving message
    :param content: Content of the resolving message
    """
    if not isinstance(rtype, MessageType):
        raise TypeError("rtype must be a MessageType")
    if content is not None and not isinstance(content, str):
        raise TypeError("content must be None or a string")
    return BaseCommand("Resolve", **{"Type": rtype, "Content": content})
