import os

from .base_connection import BaseConnection
from .. import commands, DEFAULT_BACKLOG
from ..commands import code, result
from ..commands.code_channel import CodeChannel
from ..http import HttpEndpointUnixSocket
from ..object_model import ObjectModel
from ..object_model.http_endpoints import HttpEndpointType
from ..object_model.job import GCodeFileInfo
from ..object_model.messages import MessageType
from ..object_model.state import LogLevel


class BaseCommandConnection(BaseConnection):
    """Base connection class for sending commands to the control server"""

    def add_http_endpoint(
        self,
        endpoint_type: HttpEndpointType,
        namespace: str,
        path: str,
        is_upload_request: bool = False,
        backlog: int = DEFAULT_BACKLOG,
    ):
        """Add a new third-party HTTP endpoint in the format /machine/{ns}/{path}"""
        res = self.perform_command(
            commands.http_endpoints.add_http_endpoint(endpoint_type, namespace, path, is_upload_request)
        )
        socket_file = res.result
        return HttpEndpointUnixSocket(endpoint_type, namespace, path, socket_file, backlog, self.debug)

    def add_user_session(
        self,
        access_level: commands.user_sessions.AccessLevel,
        session_type: commands.user_sessions.SessionType,
        origin: str,
    ):
        """
        Add a new user session
        :param access_level: Access level of this session
        :param session_type: Type of this session
        :param origin: Origin of the user session (e.g. IP address or PID)
        :returns: New session ID
        """
        if origin is None:
            origin = str(os.getpid())

        res = self.perform_command(commands.user_sessions.add_user_session(access_level, session_type, origin))
        return int(res.result)

    def check_password(self, password: str):
        """Check the given password (see M551)"""
        return self.perform_command(commands.generic.check_password(password))

    def evaluate_expression(self, expression, channel: CodeChannel = CodeChannel.SBC):
        """
        Evaluate an arbitrary expression
        :param expression: Expression to evaluate
        :param channel: Context of the evaluation
        :returns: Evaluation result
        """
        return self.perform_command(commands.generic.evaluate_expression(channel, expression))

    def flush(self, channel: CodeChannel = CodeChannel.SBC):
        """Wait for all pending codes of the given channel to finish"""
        return self.perform_command(commands.generic.flush(channel))

    def get_file_info(self, file_name: str, read_thumbnail_content: bool = False):
        """Parse a G-code file and returns file information about it"""
        res = self.perform_command(commands.files.get_file_info(file_name, read_thumbnail_content), GCodeFileInfo)
        return res.result

    def get_object_model(self):
        """Retrieve the full object model of the machine."""
        res = self.perform_command(commands.object_model.get_object_model(), ObjectModel)
        return res.result

    def get_serialized_object_model(self):
        """Optimized method to directly query the machine model UTF-8 JSON"""
        self.send(commands.object_model.get_object_model())
        return self.receive_json()

    def install_plugin(self, plugin_file: str):
        """Install or upgrade a plugin"""
        res = self.perform_command(commands.plugins.install_plugin(plugin_file))
        return res.result

    def install_system_package(self, package_file: str):
        """Install or upgrade a system package
        :param package_file: Absolute file path to the package file
        """
        res = self.perform_command(commands.packages.install_system_package(package_file))
        return res.result

    def invalidate_channel(self, channel: CodeChannel = CodeChannel.SBC):
        """Invalidate all pending codes and files on a given channel
        (including buffered codes from DSF in RepRapFirmware)
        :param channel: Code channel to invalidate"""
        return self.perform_command(commands.generic.invalidate_channel(channel))

    def lock_object_model(self):
        """
        Lock the machine model for read/write access.
        It is MANDATORY to call unlock_object_model when write access has finished
        """
        return self.perform_command(commands.object_model.lock_object_model())

    def patch_object_model(self, key: str, patch):
        """
        Apply a full patch to the object model. Use with care!
        """
        res = self.perform_command(commands.object_model.patch_object_model(key, patch))
        return res.result

    def perform_code(self, cde: code.Code):
        """Execute an arbitrary pre-parsed code"""
        res = self.perform_command(cde, result.CodeResult)
        return res.result

    def perform_simple_code(
        self,
        cde: str,
        channel: CodeChannel = CodeChannel.DEFAULT_CHANNEL,
        async_exec: bool = False
    ):
        """Execute an arbitrary G/M/T-code in text form
        :param cde: Code to parse and execute
        :param channel: Destination channel
        :param async_exec: Whether this code may be executed asynchronously.
                           If set, the code reply is output as a generic message
        :returns: The result as a string if async_exec is not set (default)
        """
        res = self.perform_command(commands.generic.simple_code(cde, channel, async_exec))
        return res.result

    def reload_plugin(self, plugin: str):
        """
        Reload the manifest of a given plugin. Useful for packaged plugins
        :param plugin: Identifier of the plugin
        """
        return self.perform_command(commands.plugins.reload_plugin(plugin))

    def remove_http_endpoint(self, endpoint_type: HttpEndpointType, namespace: str, path: str):
        """Remove an existing HTTP endpoint"""
        res = self.perform_command(
            commands.http_endpoints.remove_http_endpoint(endpoint_type, namespace, path)
        )
        return res.result

    def remove_user_session(self, session_id: int):
        """Remove an existing HTTP endpoint"""
        res = self.perform_command(commands.user_sessions.remove_user_session(session_id))
        return res.result

    def resolve_path(self, path: str):
        """Resolve a RepRapFirmware-style file path to a real file path"""
        return self.perform_command(commands.files.resolve_path(path))

    def set_network_protocol(self, protocol: str, enabled: bool):
        """Set a given property to a certain value.
        Make sure to lock the object model before calling this
        :param protocol: Protocol to change
        :param enabled: Whether the protocol is enabled or not
        """
        res = self.perform_command(commands.object_model.set_network_protocol(protocol, enabled))
        return res.result

    def set_object_model(self, path: str, value: str):
        """
        Set a given property to a certain value.
        Make sure to lock the object model before calling this
        """
        return self.perform_command(commands.object_model.set_object_model(path, value))

    def set_plugin_data(self, plugin: str, key: str, value: str):
        """Set custom plugin data in the object model"""
        res = self.perform_command(commands.plugins.set_plugin_data(plugin, key, value))
        return res.result

    def set_update_status(self, is_updating: bool):
        """Override the current machin staeus if a software update is in progress"""
        res = self.perform_command(commands.generic.set_update_status(is_updating))
        return res.result

    def start_plugin(self, plugin: str, save_state: bool = True):
        """Start a plugin
        :param plugin: Identifier of the plugin
        :param save_state: Defines if the list of executing plugins may be saved
        """
        res = self.perform_command(commands.plugins.start_plugin(plugin, save_state))
        return res.result

    def start_plugins(self):
        """Start all the previously started plugins again"""
        res = self.perform_command(commands.plugins.start_plugins())
        return res.result

    def stop_plugin(self, plugin: str, save_state: bool = True):
        """Stop a plugin
        :param plugin: Identifier of the plugin
        :param save_state: Defines if the list of executing plugins may be saved
        """
        res = self.perform_command(commands.plugins.stop_plugin(plugin, save_state))
        return res.result

    def stop_plugins(self):
        """Stop all the plugins and save which plugins were started before.
        This command is intended for shutdown or update requests"""
        res = self.perform_command(commands.plugins.stop_plugins())
        return res.result

    def sync_object_model(self):
        """Wait for the full object model to be updated from RepRapFirmware"""
        return self.perform_command(commands.object_model.sync_object_model())

    def uninstall_plugin(self, plugin: str):
        """Uninstall a plugin"""
        res = self.perform_command(commands.plugins.uninstall_plugin(plugin))
        return res.result

    def uninstall_system_package(self, package: str):
        """Uninstall a system package
        :param package: Identifier of the package
        """
        res = self.perform_command(commands.packages.uninstall_system_package(package))
        return res.result

    def unlock_object_model(self):
        """Unlock the object model again"""
        return self.perform_command(commands.object_model.unlock_object_model())

    def write_message(
        self,
        message_type: MessageType,
        message: str,
        output_message: bool,
        log_level: LogLevel,
    ):
        """Write an arbitrary message"""
        res = self.perform_command(
            commands.generic.write_message(message_type, message, output_message, log_level)
        )
        return res.result
