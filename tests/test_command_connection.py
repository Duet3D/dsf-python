import json
import socket
import unittest
from typing import Any, Callable

from src.dsf.commands.code_channel import CodeChannel
from src.dsf.commands.user_sessions import AccessLevel, SessionType
from src.dsf.connections import CommandConnection, InternalServerException
from src.dsf.object_model import HttpEndpointType
from src.dsf.object_model.messages import MessageType
from src.dsf.object_model.state import LogLevel


class TestCommandConnectionResults(unittest.TestCase):
    """Connection methods return the same values as DuetAPIClient"""

    def _perform(self, response: str, call: Callable[[CommandConnection], object]) -> tuple[object, dict[str, Any]]:
        """Call a connection method while DSF replies with the given response"""
        connection = CommandConnection(timeout=3)
        client, server = socket.socketpair()
        with client, server:
            connection.socket = client
            server.sendall(response.encode())
            result = call(connection)
            command: dict[str, Any] = json.loads(server.recv(65536))
        return result, command

    def test_results(self):
        cases: list[tuple[str, Callable[[CommandConnection], object], str, object]] = [
            ("CheckPassword", lambda c: c.check_password("secret"), "true", True),
            ("CheckPassword", lambda c: c.check_password("secret"), "false", False),
            ("EvaluateExpression", lambda c: c.evaluate_expression("state.upTime"), "1234", 1234),
            ("EvaluateExpression", lambda c: c.evaluate_expression("move.axes[0]"), '{"letter":"X"}', {"letter": "X"}),
            ("EvaluateExpression", lambda c: c.evaluate_expression("null"), "null", None),
            ("Flush", lambda c: c.flush(CodeChannel.FILE), "true", True),
            ("Flush", lambda c: c.flush(), "false", False),
            ("QueryObjectModel", lambda c: c.query_object_model("state"), '{"key":"state"}', {"key": "state"}),
            ("RemoveHttpEndpoint", lambda c: c.remove_http_endpoint(HttpEndpointType.GET, "ns", "path"), "true", True),
            ("RemoveUserSession", lambda c: c.remove_user_session(3), "false", False),
            ("ResolvePath", lambda c: c.resolve_path("0:/sys"), '"/opt/dsf/sd/sys"', "/opt/dsf/sd/sys"),
            ("SimpleCode", lambda c: c.perform_simple_code("M115"), '"FIRMWARE_NAME"', "FIRMWARE_NAME"),
            (
                "AddUserSession",
                lambda c: c.add_user_session(AccessLevel.READ_WRITE, SessionType.LOCAL, "test"),
                "5",
                5,
            ),
        ]
        for command, call, result, expected in cases:
            with self.subTest(command=command, result=result):
                value, sent = self._perform(f'{{"success":true,"result":{result}}}', call)
                self.assertEqual(sent["command"], command)
                self.assertEqual(value, expected)
                self.assertIs(type(value), type(expected))

    def test_no_result(self):
        # Commands without a result in DSF return None
        cases: list[tuple[str, Callable[[CommandConnection], object]]] = [
            ("InstallPlugin", lambda c: c.install_plugin("/tmp/plugin.zip")),
            ("InstallSystemPackage", lambda c: c.install_system_package("/tmp/package.deb")),
            ("InvalidateChannel", lambda c: c.invalidate_channel(CodeChannel.FILE)),
            ("PatchObjectModel", lambda c: c.patch_object_model("state", "{}")),
            ("ReloadPlugin", lambda c: c.reload_plugin("plugin")),
            ("SetNetworkProtocol", lambda c: c.set_network_protocol("http", True)),
            ("SetPluginData", lambda c: c.set_plugin_data("plugin", "key", 1)),
            ("SetUpdateStatus", lambda c: c.set_update_status(True)),
            ("SetWifiCountry", lambda c: c.set_wifi_country("GB")),
            ("StartPlugin", lambda c: c.start_plugin("plugin")),
            ("StartPlugins", lambda c: c.start_plugins()),
            ("StopPlugin", lambda c: c.stop_plugin("plugin")),
            ("StopPlugins", lambda c: c.stop_plugins()),
            ("SyncObjectModel", lambda c: c.sync_object_model()),
            ("UninstallPlugin", lambda c: c.uninstall_plugin("plugin")),
            ("UninstallSystemPackage", lambda c: c.uninstall_system_package("package")),
            ("WriteMessage", lambda c: c.write_message(MessageType.SUCCESS, "message", True, LogLevel.INFO)),
        ]
        for command, call in cases:
            with self.subTest(command=command):
                value, sent = self._perform('{"success":true}', call)
                self.assertEqual(sent["command"], command)
                self.assertIsNone(value)

    def test_unexpected_result_type(self):
        with self.assertRaisesRegex(TypeError, "Unexpected result type for Flush command"):
            self._perform('{"success":true,"result":"yes"}', lambda c: c.flush())
        with self.assertRaisesRegex(TypeError, "Unexpected result type for ResolvePath command"):
            self._perform('{"success":true,"result":null}', lambda c: c.resolve_path("0:/sys"))

    def test_error(self):
        response = '{"success":false,"errorType":"InvalidOperationException","errorMessage":"disabled"}'
        with self.assertRaises(InternalServerException) as context:
            self._perform(response, lambda c: c.flush(CodeChannel.FILE))
        self.assertEqual(context.exception.error_type, "InvalidOperationException")
        self.assertEqual(context.exception.error_message, "disabled")


if __name__ == "__main__":
    unittest.main()
