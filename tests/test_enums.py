import enum
import importlib
import json
import pkgutil
import re
import unittest
import warnings

import src.dsf as dsf
from src.dsf.commands.code_channel import CodeChannel
from src.dsf.commands.code_flags import CodeFlags
from src.dsf.commands.code_type import CodeType
from src.dsf.commands.condition_type import KeywordType
from src.dsf.connections import ConnectionMode, InterceptionMode, SubscriptionMode
from src.dsf.http import HttpResponseType
from src.dsf.object_model import HttpEndpointType, MachineStatus, PluginManifest, SbcPermissions
from src.dsf.object_model.move.axis import AxisLetter
from src.dsf.object_model.move.kinematics.kinematics_name import KinematicsName
from src.dsf.object_model.messages import MessageType
from src.dsf.object_model.sensors.probe_type import ProbeType
from src.dsf.utils import DeprecatedWarning


def _enums() -> list[type[enum.Enum]]:
    enums: list[type[enum.Enum]] = []
    for module_info in pkgutil.walk_packages(dsf.__path__, f"{dsf.__name__}."):
        module = importlib.import_module(module_info.name)
        for value in vars(module).values():
            if isinstance(value, type) and issubclass(value, enum.Enum) and value.__module__ == module.__name__:
                enums.append(value)
    return enums


class TestEnums(unittest.TestCase):
    def test_upper_snake_case(self):
        # Every member name is UPPER_SNAKE_CASE, except for the axis letters
        for cls in _enums():
            if cls is AxisLetter:
                continue
            for name, member in cls.__members__.items():
                if member.name == name:
                    with self.subTest(member=f"{cls.__name__}.{name}"):
                        self.assertRegex(name, re.compile(r"^[A-Z][A-Z0-9]*(_[A-Z0-9]+)*$"))

    def test_names(self):
        self.assertEqual(MachineStatus("changingTool").name, "CHANGING_TOOL")
        self.assertEqual(SubscriptionMode("Patch").name, "PATCH")
        self.assertEqual(KinematicsName("delta").name, "LINEAR_DELTA")
        self.assertEqual(SbcPermissions("commandExecution").name, "COMMAND_EXECUTION")
        self.assertEqual(CodeType("").name, "NONE")
        self.assertEqual(KeywordType(0).name, "NONE")
        self.assertEqual(ProbeType(0).name, "NONE")
        self.assertEqual(CodeFlags.NONE, 0)

    def test_previous_names(self):
        # The previous names are aliases of the same members and raise a DeprecatedWarning
        aliases: list[tuple[type[enum.Enum], str, enum.Enum]] = [
            (MachineStatus, "idle", MachineStatus.IDLE),
            (MachineStatus, "changingTool", MachineStatus.CHANGING_TOOL),
            (MessageType, "Success", MessageType.SUCCESS),
            (KinematicsName, "linearDelta", KinematicsName.LINEAR_DELTA),
            (CodeType, "CodeNone", CodeType.NONE),
            (CodeType, "MCode", CodeType.MCODE),
            (KeywordType, "KeywordNone", KeywordType.NONE),
            (CodeFlags, "CodeFlagsNone", CodeFlags.NONE),
            (CodeFlags, "IsLastCode", CodeFlags.IS_LAST_CODE),
            (ProbeType, "NoProbe", ProbeType.NONE),
            (ProbeType, "ScanningZProbe", ProbeType.SCANNING_ANALOG),
            (SbcPermissions, "noPermissions", SbcPermissions.NONE),
            (SbcPermissions, "commandExecution", SbcPermissions.COMMAND_EXECUTION),
            (HttpEndpointType, "WebSocket", HttpEndpointType.WEBSOCKET),
        ]
        for cls, alias, member in aliases:
            message = f"{cls.__name__}.{alias} is deprecated, use {cls.__name__}.{member.name} instead"
            with self.subTest(alias=f"{cls.__name__}.{alias}"):
                with self.assertWarnsRegex(DeprecatedWarning, message) as context:
                    self.assertIs(getattr(cls, alias), member)
                self.assertEqual(context.filename, __file__)
                with self.assertWarnsRegex(DeprecatedWarning, message) as context:
                    self.assertIs(cls[alias], member)
                self.assertEqual(context.filename, __file__)
        # Aliases are not listed as separate members
        self.assertEqual([member.name for member in MachineStatus][-1], "IDLE")
        self.assertEqual(len(list(MachineStatus)), 14)

    def test_current_names(self):
        # Current names, values and kept aliases do not raise a DeprecatedWarning
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecatedWarning)
            self.assertIs(MachineStatus.IDLE, MachineStatus["IDLE"])
            self.assertIs(MachineStatus("idle"), MachineStatus.IDLE)
            self.assertIs(CodeChannel.DEFAULT_CHANNEL, CodeChannel.SBC)
            self.assertIs(CodeChannel["DEFAULT_CHANNEL"], CodeChannel.SBC)
            self.assertEqual(SubscriptionMode.PATCH.value, "Patch")
            self.assertEqual(InterceptionMode.PRE.value, "Pre")
            self.assertEqual(ConnectionMode.COMMAND.value, "Command")
            self.assertIs(CodeFlags(2048 | 8) & CodeFlags.IS_FROM_MACRO, CodeFlags.IS_FROM_MACRO)

    def test_unknown_name(self):
        with self.assertRaises(KeyError):
            MachineStatus["unknown"]

    def test_values(self):
        # Values are the ones written by DSF
        self.assertIs(HttpEndpointType("WebSocket"), HttpEndpointType.WEBSOCKET)
        self.assertEqual(HttpResponseType.STATUS_CODE.value, "statusCode")

    def test_sbc_permissions_json(self):
        # SbcPermissions are written by value, not by name
        manifest = PluginManifest.from_json({"sbcPermissions": ["commandExecution", "objectModelRead"]})
        self.assertEqual(
            list(manifest.sbc_permissions), [SbcPermissions.COMMAND_EXECUTION, SbcPermissions.OBJECT_MODEL_READ]
        )
        self.assertEqual(json.loads(manifest.to_json())["sbcPermissions"], ["commandExecution", "objectModelRead"])


if __name__ == "__main__":
    unittest.main()
