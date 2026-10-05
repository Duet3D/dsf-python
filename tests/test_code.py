import unittest
import json
from typing import Any, cast
from unittest.mock import MagicMock

from src.dsf.commands.code import Code, CodeChannel, CodeFlags, CodeType, KeywordType
from src.dsf.commands.code_parameter import CodeParameter
from src.dsf.connections.base_connection import BaseConnection
from src.dsf.object_model.messages import Message, MessageType
from src.dsf.object_model.move.driver_id import DriverId
from src.dsf.utils import DeprecatedWarning

# Codes as written by DSF v3.7.0-rc.2 (JsonSerializer.Serialize(new Code(text), CommandContext.Default)),
# together with the text the code was parsed from
DSF_CODES = {
    "G1 X10 Y-2.5 E1:2.5 F{global.speed} ; move here": '{"command":"Code","sourceConnection":0,"result":null,"type":"G","channel":"SBC","lineNumber":null,"explicitLineNumber":null,"indent":0,"keyword":0,"keywordArgument":null,"majorNumber":1,"minorNumber":-1,"flags":2048,"comment":" move here","filePosition":null,"length":48,"parameters":[{"letter":"X","value":"10","isString":false},{"letter":"Y","value":"-2.5","isString":false},{"letter":"E","value":"1:2.5","isString":false},{"letter":"F","value":"{global.speed}","isString":false}]}',  # noqa: E501
    'M569.1 P1.2 S"a""b" T': '{"command":"Code","sourceConnection":0,"result":null,"type":"M","channel":"SBC","lineNumber":null,"explicitLineNumber":null,"indent":0,"keyword":0,"keywordArgument":null,"majorNumber":569,"minorNumber":1,"flags":2048,"comment":null,"filePosition":null,"length":22,"parameters":[{"letter":"P","value":"1.2","isDriverId":true,"isString":false},{"letter":"S","value":"a\\"b","isString":true},{"letter":"T","value":"","isString":false}]}',  # noqa: E501
    "if move.axes[0].homed": '{"command":"Code","sourceConnection":0,"result":null,"type":"K","channel":"SBC","lineNumber":null,"explicitLineNumber":null,"indent":0,"keyword":1,"keywordArgument":"move.axes[0].homed","majorNumber":null,"minorNumber":-1,"flags":2048,"comment":null,"filePosition":null,"length":22,"parameters":[]}',  # noqa: E501
    "; just a comment": '{"command":"Code","sourceConnection":0,"result":null,"type":"Q","channel":"SBC","lineNumber":null,"explicitLineNumber":null,"indent":0,"keyword":0,"keywordArgument":null,"majorNumber":null,"minorNumber":-1,"flags":2048,"comment":" just a comment","filePosition":null,"length":17,"parameters":[]}',  # noqa: E501
    "M584 X0.1:0.2": '{"command":"Code","sourceConnection":0,"result":null,"type":"M","channel":"SBC","lineNumber":null,"explicitLineNumber":null,"indent":0,"keyword":0,"keywordArgument":null,"majorNumber":584,"minorNumber":-1,"flags":2048,"comment":null,"filePosition":null,"length":14,"parameters":[{"letter":"X","value":"0.1:0.2","isDriverId":true,"isString":false}]}',  # noqa: E501
    "G53 G1 X1": '{"command":"Code","sourceConnection":0,"result":null,"type":"G","channel":"SBC","lineNumber":null,"explicitLineNumber":null,"indent":0,"keyword":0,"keywordArgument":null,"majorNumber":1,"minorNumber":-1,"flags":2176,"comment":null,"filePosition":null,"length":10,"parameters":[{"letter":"X","value":"1","isString":false}]}',  # noqa: E501
    'M117 "hello world"': '{"command":"Code","sourceConnection":0,"result":null,"type":"M","channel":"SBC","lineNumber":null,"explicitLineNumber":null,"indent":0,"keyword":0,"keywordArgument":null,"majorNumber":117,"minorNumber":-1,"flags":2048,"comment":null,"filePosition":null,"length":19,"parameters":[{"letter":"@","value":"hello world","isString":true}]}',  # noqa: E501
    "G1 X1": '{"command":"Code","sourceConnection":0,"result":null,"type":"G","channel":"SBC","lineNumber":123,"explicitLineNumber":123,"indent":0,"keyword":0,"keywordArgument":null,"majorNumber":1,"minorNumber":-1,"flags":10240,"comment":null,"filePosition":null,"length":11,"parameters":[{"letter":"X","value":"1","isString":false}]}',  # noqa: E501
}


class Model(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_code(self):
        json_str = '{"sourceConnection":30,"result":null,"type":"M","channel":"HTTP","lineNumber":null,"indent":0,"keyword":0,"keywordArgument":null,"majorNumber":98,"minorNumber":null,"flags":2048,"comment":null,"filePosition":null,"length":22,"parameters":[{"letter":"P","value":"0:/macros/test","isString":true}],"command":"Code"}'
        c = Code.from_json(json.loads(json_str))
        self.assertEqual(str(c), 'M98 P"0:/macros/test"')
        self.assertEqual(c.type, CodeType.MCODE)
        self.assertEqual(c.major_number, 98)
        self.assertEqual(c.minor_number, -1)
        self.assertEqual(c.flags, CodeFlags.IS_LAST_CODE)
        self.assertEqual(c.keyword, KeywordType.NONE)
        self.assertEqual(c.keyword_argument, None)
        self.assertEqual(c.comment, None)
        self.assertEqual(c.length, 22)
        self.assertEqual(c.line_number, None)
        self.assertEqual(c.file_position, None)
        self.assertEqual(c.indent, 0)
        self.assertEqual(c.channel, CodeChannel.HTTP)
        self.assertEqual(c.source_connection, 30)
        self.assertEqual(c.command, "Code")

    def test_code_keyword(self):
        json_str = '{"sourceConnection":33,"result":null,"type":"K","channel":"HTTP","lineNumber":null,"indent":0,"keyword":9,"keywordArgument":"test","majorNumber":null,"minorNumber":null,"flags":2048,"comment":null,"filePosition":null,"length":12,"parameters":[],"command":"Code"}'
        c = Code.from_json(json.loads(json_str))
        self.assertEqual(c.type, CodeType.KEYWORD)
        self.assertEqual(c.keyword, KeywordType.ECHO)

    def test_dsf_codes(self):
        # Codes written by DSF are converted back to the same JSON and text
        for text, json_str in DSF_CODES.items():
            with self.subTest(code=text):
                data = json.loads(json_str)
                c = Code.from_json(data)
                self.assertEqual(json.loads(c.to_json()), data)
                self.assertEqual(str(c), text)

    def test_parameters(self):
        c = Code.from_json(json.loads(DSF_CODES['M569.1 P1.2 S"a""b" T']))
        self.assertEqual(c.minor_number, 1)
        driver, text = c.parameter("P"), c.parameter("S")
        assert driver is not None and text is not None
        self.assertEqual(driver.value, DriverId(board=1, port=2))
        self.assertEqual(text.value, 'a"b')

    def test_explicit_line_number(self):
        c = Code.from_json(json.loads(DSF_CODES["G1 X1"]))
        self.assertEqual(c.line_number, 123)
        self.assertEqual(c.explicit_line_number, 123)
        c.flags = CodeFlags.IS_LAST_CODE
        self.assertEqual(c.explicit_line_number, None)

    def test_flags(self):
        # DSF sends several flags as one number
        c = Code.from_json({"type": "G", "majorNumber": 1, "flags": 2048 | 8})
        self.assertTrue(c.is_flag_set(CodeFlags.IS_LAST_CODE))
        self.assertTrue(c.is_flag_set(CodeFlags.IS_FROM_MACRO))
        self.assertFalse(c.is_flag_set(CodeFlags.IS_FROM_CONFIG))

    def test_result(self):
        data: dict[str, Any] = json.loads(DSF_CODES["G1 X1"])
        data["result"] = {"type": 1, "content": "homed", "time": "2026-10-05T12:00:00"}
        c = Code.from_json(data)
        assert c.result is not None
        self.assertEqual(c.result.type, MessageType.WARNING)
        self.assertEqual(c.result.content, "homed")
        self.assertEqual(str(c), "G1 X1 => Warning: homed")
        self.assertEqual(json.loads(c.to_json())["result"], data["result"])

    def test_new_code(self):
        # Codes created in Python are written the same way as DSF writes them
        c = Code(
            type=CodeType.MCODE,
            major_number=569,
            minor_number=1,
            parameters=[
                CodeParameter("X", 10),
                CodeParameter("E", [1.0, 2.5]),
                CodeParameter("P", DriverId(as_str="1.2")),
                CodeParameter("Q", [DriverId(as_str="0.1"), DriverId(as_str="0.2")]),
                CodeParameter("S", 'a"b'),
                CodeParameter("F", "{global.speed}"),
                CodeParameter.simple_param("@", "hello"),
            ],
        )
        self.assertEqual(str(c), 'M569.1 X10 E1.0:2.5 P1.2 Q0.1:0.2 S"a""b" F{global.speed} "hello"')
        self.assertEqual(
            c.to_dict()["parameters"],
            [
                {"letter": "X", "value": "10", "isString": False},
                {"letter": "E", "value": "1.0:2.5", "isString": False},
                {"letter": "P", "value": "1.2", "isDriverId": True, "isString": False},
                {"letter": "Q", "value": "0.1:0.2", "isDriverId": True, "isString": False},
                {"letter": "S", "value": 'a"b', "isString": True},
                {"letter": "F", "value": "{global.speed}", "isString": False},
                {"letter": "@", "value": "hello", "isString": True},
            ],
        )

    def test_send(self):
        # Connections send codes in the format DSF reads them
        c = Code.from_json(json.loads(DSF_CODES["G1 X10 Y-2.5 E1:2.5 F{global.speed} ; move here"]))
        c.result = Message(MessageType.ERROR, "failed")
        connection = BaseConnection()
        connection.socket = MagicMock()
        connection.send(c)
        sent = json.loads(connection.socket.sendall.call_args.args[0])
        self.assertEqual(sent, json.loads(c.to_json()))

    def test_constructor_defaults(self):
        c = Code()
        self.assertEqual(c.command, "Code")
        self.assertEqual(c.type, CodeType.NONE)
        self.assertEqual(c.major_number, None)
        self.assertEqual(c.minor_number, -1)
        self.assertEqual(c.parameters, [])
        self.assertEqual(c.channel, CodeChannel.DEFAULT_CHANNEL)
        self.assertEqual(c.keyword, KeywordType.NONE)
        self.assertEqual(c.keyword_argument, None)
        self.assertEqual(c.flags, CodeFlags.NONE)
        self.assertEqual(c.comment, None)
        self.assertEqual(c.line_number, None)
        self.assertEqual(c.indent, 0)
        self.assertEqual(c.file_position, None)
        self.assertEqual(c.length, None)
        self.assertEqual(c.source_connection, 0)
        self.assertEqual(c.result, None)
        self.assertEqual(str(c), "")
        # Each code gets its own parameter list
        c.parameters.append(CodeParameter("X", 1))
        self.assertEqual(Code().parameters, [])

    def test_constructor(self):
        parameters = [CodeParameter("X", 10)]
        result = Message(MessageType.WARNING, "done")
        c = Code(
            type=CodeType.GCODE,
            major_number=54,
            minor_number=3,
            parameters=parameters,
            channel=CodeChannel.FILE,
            keyword=KeywordType.NONE,
            keyword_argument="arg",
            flags=CodeFlags.IS_FROM_MACRO | CodeFlags.HAS_EXPLICIT_LINE_NUMBER,
            comment="comment",
            line_number=12,
            indent=4,
            file_position=345,
            length=6,
            source_connection=7,
            result=result,
        )
        self.assertEqual(c.command, "Code")
        self.assertEqual(c.type, CodeType.GCODE)
        self.assertEqual(c.major_number, 54)
        self.assertEqual(c.minor_number, 3)
        self.assertIs(c.parameters, parameters)
        self.assertEqual(c.channel, CodeChannel.FILE)
        self.assertEqual(c.keyword, KeywordType.NONE)
        self.assertEqual(c.keyword_argument, "arg")
        self.assertEqual(c.flags, CodeFlags.IS_FROM_MACRO | CodeFlags.HAS_EXPLICIT_LINE_NUMBER)
        self.assertEqual(c.comment, "comment")
        self.assertEqual(c.line_number, 12)
        self.assertEqual(c.explicit_line_number, 12)
        self.assertEqual(c.indent, 4)
        self.assertEqual(c.file_position, 345)
        self.assertEqual(c.length, 6)
        self.assertEqual(c.source_connection, 7)
        self.assertIs(c.result, result)
        self.assertTrue(c.is_from_file_channel)
        self.assertEqual(str(c), "G54.3 X10 ;comment => Warning: done")
        self.assertEqual(
            c.to_dict(),
            {
                "command": "Code",
                "sourceConnection": 7,
                "result": json.loads(result.to_json()),
                "type": "G",
                "channel": "File",
                "lineNumber": 12,
                "explicitLineNumber": 12,
                "indent": 4,
                "keyword": 0,
                "keywordArgument": "arg",
                "majorNumber": 54,
                "minorNumber": 3,
                "flags": 8 | 8192,
                "comment": "comment",
                "filePosition": 345,
                "length": 6,
                "parameters": [{"letter": "X", "value": "10", "isString": False}],
            },
        )

    def test_deprecated_aliases(self):
        aliases: dict[str, tuple[str, object, object]] = {
            # alias: (attribute, value set by the constructor, new value)
            "sourceConnection": ("source_connection", 7, 8),
            "lineNumber": ("line_number", 12, 13),
            "keywordArgument": ("keyword_argument", "arg", "new arg"),
            "majorNumber": ("major_number", 54, 55),
            "minorNumber": ("minor_number", 3, 4),
            "filePosition": ("file_position", 345, 346),
        }
        for alias, (name, value, new_value) in aliases.items():
            with self.subTest(alias=alias):
                c = Code(**cast(dict[str, Any], {name: value}))
                with self.assertWarnsRegex(DeprecatedWarning, f"Code.{alias} is deprecated, use Code.{name} instead"):
                    self.assertEqual(getattr(c, alias), value)
                with self.assertWarnsRegex(DeprecatedWarning, f"Code.{alias} is deprecated, use Code.{name} instead"):
                    setattr(c, alias, new_value)
                self.assertEqual(getattr(c, name), new_value)
                # The alias does not create a separate attribute
                self.assertNotIn(alias, vars(c))

    def test_deprecated_alias_warning_location(self):
        # The warning points at the code that uses the alias
        c = Code(major_number=1)
        with self.assertWarns(DeprecatedWarning) as context:
            c.majorNumber
        self.assertEqual(context.filename, __file__)
        with self.assertWarns(DeprecatedWarning) as context:
            c.majorNumber = 2
        self.assertEqual(context.filename, __file__)
