import os

from typing import Optional, TypeVar

from .base_connection import BaseConnection
from .exceptions import InternalServerException
from .. import commands, DEFAULT_BACKLOG
from ..commands import code
from ..commands.base_command import BaseCommand
from ..commands.code_channel import CodeChannel
from ..commands.file_directory import FileDirectory
from ..http import HttpEndpointUnixSocket
from ..object_model import HttpEndpointType, ObjectModel
from ..object_model.job import GCodeFileInfo
from ..object_model.messages import Message, MessageType
from ..object_model.state import LogLevel
from ..utils import JSONElement

T = TypeVar("T")


class BaseCommandConnection(BaseConnection):
    """Base connection class for sending commands to the control server"""

    def _perform_command_with_result(self, command: BaseCommand, result_type: type[T]) -> T:
        """Perform a command and check the type of its result"""
        res = self.perform_command(command)
        if not isinstance(res.result, result_type):
            raise TypeError(f"Unexpected result type for {command.command} command: {type(res.result)}")
        return res.result

    def add_http_endpoint(
        self,
        endpoint_type: HttpEndpointType,
        namespace: str,
        path: str,
        is_upload_request: bool = False,
        backlog: int = DEFAULT_BACKLOG,
    ) -> HttpEndpointUnixSocket:
        """Add a new third-party HTTP endpoint in the format /machine/{ns}/{path}"""
        socket_file = self._perform_command_with_result(
            commands.http_endpoints.add_http_endpoint(endpoint_type, namespace, path, is_upload_request), str
        )
        return HttpEndpointUnixSocket(endpoint_type, namespace, path, socket_file, backlog, self.debug)

    def add_user_session(
        self,
        access_level: commands.user_sessions.AccessLevel,
        session_type: commands.user_sessions.SessionType,
        origin: Optional[str],
    ) -> int:
        """
        Add a new user session
        :param access_level: Access level of this session
        :param session_type: Type of this session
        :param origin: Origin of the user session (e.g. IP address or PID)
        :returns: New session ID
        """
        if origin is None:
            origin = str(os.getpid())

        return self._perform_command_with_result(
            commands.user_sessions.add_user_session(access_level, session_type, origin), int
        )

    def check_password(self, password: str) -> bool:
        """
        Check the given password (see M551)
        :returns: True if the password is correct or no password is set
        """
        return self._perform_command_with_result(commands.generic.check_password(password), bool)

    def evaluate_expression(self, expression: str, channel: CodeChannel = CodeChannel.SBC) -> JSONElement:
        """
        Evaluate an arbitrary expression
        :param expression: Expression to evaluate
        :param channel: Context of the evaluation
        :returns: Evaluation result
        """
        return self.perform_command(commands.generic.evaluate_expression(channel, expression)).result

    def flush(self, channel: CodeChannel = CodeChannel.SBC) -> bool:
        """
        Wait for all pending codes of the given channel to finish
        :returns: True if the flush request was successful
        """
        return self._perform_command_with_result(commands.generic.flush(channel), bool)

    def get_file_info(self, file_name: str, read_thumbnail_content: bool = False) -> GCodeFileInfo:
        """Parse a G-code file and returns file information about it"""
        command = commands.files.get_file_info(file_name, read_thumbnail_content)
        res = self.perform_command(command, GCodeFileInfo)
        if res.result is None:
            raise InternalServerException(command, "InvalidResponseType", "Expected file info, got null")
        return res.result

    def get_object_model(self, filters: list[str] = []) -> ObjectModel:
        """
        Retrieve the full object model of the machine.

        :param filters: Optional object model key paths to retrieve.
                        If any key paths are given, the returned instance holds only the requested parts and every other
                        property is left at its default value. There is no way to tell those apart from values that are
                        genuinely unset.
        """
        command = commands.object_model.get_object_model(filters)
        res = self.perform_command(command, ObjectModel)
        if res.result is None:
            raise InternalServerException(command, "InvalidResponseType", "Expected object model, got null")
        return res.result

    def get_serialized_object_model(self) -> str:
        """Optimized method to directly query the machine model UTF-8 JSON"""
        self.send(commands.object_model.get_object_model())
        return self.receive_json()

    def install_plugin(self, plugin_file: str) -> None:
        """Install or upgrade a plugin"""
        self.perform_command(commands.plugins.install_plugin(plugin_file))

    def install_system_package(self, package_file: str) -> None:
        """Install or upgrade a system package
        :param package_file: Absolute file path to the package file
        """
        self.perform_command(commands.packages.install_system_package(package_file))

    def invalidate_channel(self, channel: CodeChannel = CodeChannel.SBC) -> None:
        """Invalidate all pending codes and files on a given channel
        (including buffered codes from DSF in RepRapFirmware)
        :param channel: Code channel to invalidate"""
        self.perform_command(commands.generic.invalidate_channel(channel))

    def query_object_model(self, key: str = "", flags: str = "") -> JSONElement:
        """
        Query the object model using a key and flags, returning a formatted JSON response
        compatible with the M409 response format without going through the code execution pipeline
        :param key: Object model key path to query (e.g. "heat", "move.axes", "" for root)
        :param flags: RRF-compatible flags string controlling response content (see M409 F parameter)
        :returns: M409-compatible JSON response
        """
        return self.perform_command(commands.object_model.query_object_model(key, flags)).result

    def patch_object_model(self, key: str, patch: str) -> None:
        """
        Apply a full patch to the object model. Use with care!
        """
        self.perform_command(commands.object_model.patch_object_model(key, patch))

    def perform_code(self, cde: code.Code) -> Optional[Message]:
        """Execute an arbitrary pre-parsed code
        :returns: The code result or None if there is none"""
        res = self.perform_command(cde, Message)
        return res.result

    def perform_simple_code(
        self, cde: str, channel: CodeChannel = CodeChannel.DEFAULT_CHANNEL, async_exec: bool = False
    ) -> str:
        """Execute an arbitrary G/M/T-code in text form

        :param cde: Code to parse and execute
        :param channel: Destination channel
        :param async_exec: Whether this code may be executed asynchronously.
                           If set, the code reply is output as a generic message
        :returns: The result as a string if async_exec is not set (default)
        """
        return self._perform_command_with_result(commands.generic.simple_code(cde, channel, async_exec), str)

    def reload_plugin(self, plugin: str) -> None:
        """
        Reload the manifest of a given plugin. Useful for packaged plugins
        :param plugin: Identifier of the plugin
        """
        self.perform_command(commands.plugins.reload_plugin(plugin))

    def remove_http_endpoint(self, endpoint_type: HttpEndpointType, namespace: str, path: str) -> bool:
        """
        Remove an existing HTTP endpoint
        :returns: True if the endpoint could be removed
        """
        return self._perform_command_with_result(
            commands.http_endpoints.remove_http_endpoint(endpoint_type, namespace, path), bool
        )

    def remove_user_session(self, session_id: int) -> bool:
        """
        Remove an existing user session
        :returns: True if the session could be removed
        """
        return self._perform_command_with_result(commands.user_sessions.remove_user_session(session_id), bool)

    def resolve_path(self, path: str, base_directory: Optional[FileDirectory] = None) -> str:
        """Resolve a RepRapFirmware-style file path to a real file path
        :param path: File path to resolve
        :param base_directory: Optional base directory to resolve the path relative to
        """
        return self._perform_command_with_result(commands.files.resolve_path(path, base_directory), str)

    def set_network_protocol(self, protocol: str, enabled: bool) -> None:
        """Set a given property to a certain value.
        Make sure to lock the object model before calling this
        :param protocol: Protocol to change
        :param enabled: Whether the protocol is enabled or not
        """
        self.perform_command(commands.object_model.set_network_protocol(protocol, enabled))

    def set_wifi_country(self, country_code: Optional[str] = None) -> None:
        """
        Set the WiFi country code. This is a global setting on Linux, so it is applied to every WiFi interface
        in the object model
        :param country_code: New WiFi country code, or null to clear it
        """
        self.perform_command(commands.object_model.set_wifi_country(country_code))

    def set_plugin_data(self, plugin: str, key: str, value: object) -> None:
        """Set custom plugin data in the object model"""
        self.perform_command(commands.plugins.set_plugin_data(plugin, key, value))

    def set_update_status(self, is_updating: bool, message: str = "", progress: Optional[float] = None) -> None:
        """
        Override the current machine status if a software update is in progress
        :param is_updating: Whether an update is now in progress
        :param message: Description of the current update step, only used if is_updating is true
        :param progress: Progress of the current update step (0..1) or None if indeterminate,
            only used if is_updating is true
        """
        self.perform_command(commands.generic.set_update_status(is_updating, message, progress))

    def start_plugin(self, plugin: str, save_state: bool = True) -> None:
        """Start a plugin
        :param plugin: Identifier of the plugin
        :param save_state: Defines if the list of executing plugins may be saved
        """
        self.perform_command(commands.plugins.start_plugin(plugin, save_state))

    def start_plugins(self) -> None:
        """Start all the previously started plugins again"""
        self.perform_command(commands.plugins.start_plugins())

    def stop_plugin(self, plugin: str, save_state: bool = True) -> None:
        """Stop a plugin
        :param plugin: Identifier of the plugin
        :param save_state: Defines if the list of executing plugins may be saved
        """
        self.perform_command(commands.plugins.stop_plugin(plugin, save_state))

    def stop_plugins(self) -> None:
        """Stop all the plugins and save which plugins were started before.
        This command is intended for shutdown or update requests"""
        self.perform_command(commands.plugins.stop_plugins())

    def sync_object_model(self) -> None:
        """Wait for the full object model to be updated from RepRapFirmware"""
        self.perform_command(commands.object_model.sync_object_model())

    def uninstall_plugin(self, plugin: str) -> None:
        """Uninstall a plugin"""
        self.perform_command(commands.plugins.uninstall_plugin(plugin))

    def uninstall_system_package(self, package: str) -> None:
        """Uninstall a system package
        :param package: Identifier of the package
        """
        self.perform_command(commands.packages.uninstall_system_package(package))

    def write_message(
        self,
        message_type: MessageType,
        message: str,
        output_message: bool,
        log_level: LogLevel,
    ) -> None:
        """Write an arbitrary message"""
        self.perform_command(commands.generic.write_message(message_type, message, output_message, log_level))
