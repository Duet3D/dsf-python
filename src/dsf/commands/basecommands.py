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

from .codechannel import CodeChannel


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
    return BaseCommand("Acknowledge")


def cancel():
    return BaseCommand("Cancel")


def ignore():
    return BaseCommand("Ignore")


def get_machine_model():
    return BaseCommand("GetObjectModel")


def get_object_model():
    return BaseCommand("GetObjectModel")


def sync_machine_model():
    return BaseCommand("SyncObjectModel")


def sync_object_model():
    return BaseCommand("SyncObjectModel")


def lock_machine_model():
    return BaseCommand("LockObjectModel")


def lock_object_model():
    return BaseCommand("LockObjectModel")


def unlock_machine_model():
    return BaseCommand("UnlockObjectModel")


def unlock_object_model():
    return BaseCommand("UnlockObjectModel")


def add_http_endpoint(
    endpoint_type: HttpEndpointType, namespace: str, path: str, is_upload_request: bool
):
    """
    Register a new HTTP endpoint via DuetWebServer.
    This will create a new HTTP endpoint under /machine/{Namespace}/{EndpointPath}.
    Returns a path to the UNIX socket which DuetWebServer will connect to whenever a matching
    HTTP request is received. A plugin using this command has to open a new UNIX socket with
    the given path that DuetWebServer can connect to
    """
    if not isinstance(endpoint_type, HttpEndpointType):
        raise TypeError("endpoint_type must be a HttpEndpointType")
    if not isinstance(namespace, str) or not namespace:
        raise TypeError("namespace must be a string")
    if not isinstance(path, str) or not path:
        raise TypeError("path must be a string")
    if not isinstance(is_upload_request, bool):
        raise TypeError("is_upload_request must be a bool")
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
    Returns true if the endpoint could be successfully removed
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
    """Remove an existing user session"""
    if not isinstance(session_id, int):
        raise TypeError("session_id must be an int")
    return BaseCommand("RemoveUserSession", **{"Id": session_id})


def evaluate_expression(channel: CodeChannel, expression: str):
    """
    Evaluate an arbitrary expression on the given channel in RepRapFirmware.
    Do not use this call to evaluate file-based and network-related fields because the
    DSF and RRF models diverge in this regard.
    """
    if not isinstance(channel, CodeChannel):
        raise TypeError("channel must be a CodeChannel")
    if not isinstance(expression, str) or not expression:
        raise TypeError("expression must be a string")
    return BaseCommand(
        "EvaluateExpression", **{"Channel": channel, "Expression": expression}
    )


def flush(channel: CodeChannel):
    """Create a Flush command"""
    if not isinstance(channel, CodeChannel):
        raise TypeError("channel must be a CodeChannel")
    return BaseCommand("Flush", **{"Channel": channel})


def get_file_info(file_name: str):
    """Create a GetFileInfo command"""
    if not isinstance(file_name, str) or not file_name:
        raise TypeError("file_name must be a string")
    return BaseCommand("GetFileInfo", **{"FileName": file_name})


def resolve_path(path: str):
    """Create a ResolvePath command"""
    if not isinstance(path, str) or not path:
        raise TypeError("path must be a string")
    return BaseCommand("ResolvePath", **{"Path": path})


def simple_code(code: str, channel: CodeChannel):
    """Create a simple G/M/T code command"""
    if not isinstance(code, str) or not code:
        raise TypeError("code must be a string")
    if not isinstance(channel, CodeChannel):
        raise TypeError("channel must be a CodeChannel")
    return BaseCommand("SimpleCode", **{"Code": code, "Channel": channel})


def patch_object_model(key: str, patch: str):
    """
    Apply a full patch to the object model. May be used only in non-SPI mode
    """
    if not isinstance(key, str) or not key:
        raise TypeError("key must be a string")
    if not isinstance(patch, str) or not patch:
        raise TypeError("patch must be a string")
    return BaseCommand("PatchObjectModel", **{"Key": key, "Patch": patch})


def set_object_model(property_path: str, value: str):
    """
    Set an atomic property in the object model.
    Make sure to acquire the read/write lock first! Returns true if the field could be updated
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
    Override the current status as reported by the object model when
    performing a software update.
    """
    if not isinstance(updating, bool):
        raise TypeError("updating must be a bool")
    return BaseCommand("SetUpdateStatus", **{"Updating": updating})


def install_plugin(plugin_file: str):
    """
    Install or upgrade a plugin
    """
    if not isinstance(plugin_file, str) or not plugin_file:
        raise TypeError("plugin_file must be a string")
    return BaseCommand("InstallPlugin", **{"PluginFile": plugin_file})


def set_plugin_data(plugin: str, key: str, value: str):
    """
    Set custom plugin data in the object model.
    May be used to update only the own plugin data unless the plugin has the ManagePlugins permission
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
    """
    if not isinstance(plugin, str) or not plugin:
        raise TypeError("plugin must be a string")
    return BaseCommand("StartPlugin", **{"Plugin": plugin})


def stop_plugin(plugin: str):
    """
    Stop a plugin
    """
    if not isinstance(plugin, str) or not plugin:
        raise TypeError("plugin must be a string")
    return BaseCommand("StopPlugin", **{"Plugin": plugin})


def uninstall_plugin(plugin: str):
    """
    Uninstall a plugin
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
    """Create a Resolve message"""
    if not isinstance(rtype, MessageType):
        raise TypeError("rtype must be a MessageType")
    if content is not None and not isinstance(content, str):
        raise TypeError("content must be None or a string")
    return BaseCommand("Resolve", **{"Type": rtype, "Content": content})
