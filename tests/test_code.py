import unittest
import json

from src.dsf.commands.code import Code, CodeChannel, CodeFlags, CodeType, KeywordType


class Model(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_code(self):
        json_str = '{"sourceConnection":30,"result":null,"type":"M","channel":"HTTP","lineNumber":null,"indent":0,"keyword":0,"keywordArgument":null,"majorNumber":98,"minorNumber":null,"flags":2048,"comment":null,"filePosition":null,"length":22,"parameters":[{"letter":"P","value":"0:/macros/test","isString":true}],"command":"Code"}'
        c = Code.from_json(json.loads(json_str))
        self.assertEqual(str(c), 'M98 P"0:/macros/test"')
        self.assertEqual(c.type, CodeType.MCode)
        self.assertEqual(c.majorNumber, 98)
        self.assertEqual(c.minorNumber, None)
        self.assertEqual(c.flags, CodeFlags.IsLastCode)
        self.assertEqual(c.keyword, KeywordType.KeywordNone)
        self.assertEqual(c.keywordArgument, None)
        self.assertEqual(c.comment, None)
        self.assertEqual(c.length, 22)
        self.assertEqual(c.lineNumber, None)
        self.assertEqual(c.filePosition, None)
        self.assertEqual(c.indent, 0)
        self.assertEqual(c.channel, CodeChannel.HTTP)
        self.assertEqual(c.command, 'Code')

    def test_code_keyword(self):
        json_str = '{"sourceConnection":33,"result":null,"type":"K","channel":"HTTP","lineNumber":null,"indent":0,"keyword":9,"keywordArgument":"test","majorNumber":null,"minorNumber":null,"flags":2048,"comment":null,"filePosition":null,"length":12,"parameters":[],"command":"Code"}'
        c = Code.from_json(json.loads(json_str))
        self.assertEqual(c.type, CodeType.Keyword)
        self.assertEqual(c.keyword, KeywordType.Echo)
