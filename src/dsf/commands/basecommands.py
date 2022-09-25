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
from warnings import warn


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


DEPRECATED_NAMES = [
    ("get_machine_model", "object_model.get_object_model"),
    ("sync_machine_model", "object_model.sync_object_model"),
    ("lock_machine_model", "object_model.lock_object_model"),
    ("unlock_machine_model", "object_model.unlock_object_model")
]


MOVED_NAMES = [
    # code_interception
    ("cancel", "code_interception"),
    ("ignore", "code_interception"),
    ("resolve_code", "code_interception"),
    # files
    ("get_file_info", "files"),
    ("resolve_path", "files"),
    # generic
    ("check_password", "generic"),
    ("evaluate_expression", "generic"),
    ("flush", "generic"),
    ("set_update_status", "generic"),
    ("simple_code", "generic"),
    ("write_message", "generic"),
    # http_endpoints
    ("HttpEndpointType", "http_endpoints"),
    ("add_http_endpoint", "http_endpoints"),
    ("remove_http_endpoint", "http_endpoints"),
    # model_subscription
    ("acknowledge", "model_subscription"),
    # object_model
    ("get_object_model", "object_model"),
    ("lock_object_model", "object_model"),
    ("patch_object_model", "object_model"),
    ("set_object_model", "object_model"),
    ("sync_object_model", "object_model"),
    ("unlock_object_model", "object_model"),
    # plugins
    ("install_plugin", "plugins"),
    ("set_plugin_data", "plugins"),
    ("start_plugin", "plugins"),
    ("stop_plugin", "plugins"),
    ("uninstall_plugin", "plugins"),
    # user_sessions
    ("AccessLevel", "user_sessions"),
    ("SessionType", "user_sessions"),
    ("add_user_session", "user_sessions"),
    ("remove_user_session", "user_sessions"),
]


def __getattr__(name):
    for old_name, new_name in DEPRECATED_NAMES:
        if name == old_name:
            msg = f"{name} is deprecated and is going to be removed in the next release."
            if len(new_name):
                msg += f" Please use {new_name} instead."
            warn(msg, FutureWarning, stacklevel=2)
            return globals()[f"_deprecated_{name}"]

    for old_name, new_module in MOVED_NAMES:
        if name == old_name:
            msg = f"{name} has been moved and is going to be removed in the next release." \
                  f" Please call {name} from commands.{new_module} module instead."
            warn(msg, FutureWarning, stacklevel=2)
            _temp = __import__(f"dsf.commands.{new_module}", globals(), locals(), [name], 0)
            return getattr(_temp, name)

    raise AttributeError(f"module {__name__} has no attribute {name}")


def _deprecated_get_machine_model():
    return BaseCommand("GetObjectModel")


def _deprecated_sync_machine_model():
    return BaseCommand("SyncObjectModel")


def _deprecated_lock_machine_model():
    return BaseCommand("LockObjectModel")


def _deprecated_unlock_machine_model():
    return BaseCommand("UnlockObjectModel")
