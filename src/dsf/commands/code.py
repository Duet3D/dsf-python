from typing import List, Optional

from .base_command import BaseCommand
from .code_channel import CodeChannel
from .code_flags import CodeFlags
from .code_parameter import CodeParameter
from .code_type import CodeType
from .condition_type import KeywordType
from ..object_model.messages import Message


class Code(BaseCommand):
    """A parsed representation of a generic G/M/T-code"""

    @classmethod
    def from_json(cls, data):
        """Deserialize an instance of this class from JSON deserialized dictionary"""
        data["result"] = None if data["result"] is None else list(map(Message.from_json, data["result"]))
        data["parameters"] = list(map(CodeParameter.from_json, data["parameters"]))
        if "channel" in data:
            data["channel"] = CodeChannel(data["channel"])
        return cls(**data)

    def __init__(self, **kwargs):
        # The connection ID this code was received from. If this is 0, the code originates from an internal DCS task
        # Usually there is no need to populate this property.
        # It is internally overwritten by the control server on receipt
        self.sourceConnection = 0

        # Result of this code. This property is only set when the code has finished its execution.
        # It remains None if the code has been cancelled
        self.result: Optional[List[Message]] = None

        # Type of the code
        self.type = CodeType.CodeNone

        # Code channel to send this code to
        self.channel = CodeChannel.DEFAULT_CHANNEL

        # Line number of this code
        self.lineNumber = None

        # Number of whitespaces prefixing the command content
        self.indent = 0

        # Type of conditional G-code (if any)
        self.keyword = KeywordType.KeywordNone

        # Argument of the conditional G-code (if any)
        self.keywordArgument = None

        # Major code number (e.g. 28 in G28)
        self.majorNumber = None

        # Minor code number (e.g. 3 in G54.3)
        self.minorNumber = None

        # Flags of this code
        self.flags = CodeFlags.CodeFlagsNone

        # Comment of the G/M/T-code. May be null if no comment is present
        # The parser combines different comment segments and concatenates them as a single value.
        # So for example a code like 'G28 (Do homing) ; via G28'
        # causes the Comment field to be filled with 'Do homing via G28'
        self.comment = None

        # File position of this code in bytes (optional)
        self.filePosition = None

        # Length of the original code in bytes (optional)
        self.length = None

        # List of parsed code parameters
        self.parameters: List[CodeParameter] = []

        super().__init__(**kwargs)

    @property
    def is_from_file_channel(self) -> bool:
        """Check if this code is from a file channel"""
        return self.channel is CodeChannel.File or self.channel is CodeChannel.File2

    def parameter(self, letter: str, default=None):
        """Retrieve the parameter whose letter equals c or generate a default parameter"""
        letter = letter.upper()
        param = [param for param in self.parameters if param.letter.upper() == letter]
        if len(param) > 0:
            return param[0]
        if default is not None:
            return CodeParameter.simple_param(letter, default)
        return None

    def get_unprecedented_string(self, quote: bool = False):
        """
        Reconstruct an unprecedented string from the parameter list or
        retrieve the parameter which does not have a letter assigned.
        """
        str_list = []
        for param in self.parameters:
            if quote and param.is_string:
                str_list.append(f'{param.letter}"{param.string_value}"')
            else:
                str_list.append(f"{param.letter}{param.string_value}")
        return " ".join(str_list)

    def __str__(self):
        """Convert the parsed code back to a text-based G/M/T-code"""
        if self.keyword != KeywordType.KeywordNone:
            if self.keywordArgument is not None:
                return f"{self.keyword_to_str()} {self.keywordArgument}"
            else:
                return self.keyword_to_str()

        if self.type == CodeType.Comment:
            return f";{self.comment}"

        str_list = [self.short_str()]

        for param in self.parameters:
            str_list.append(f" {param}")

        if self.comment:
            if len(str_list) > 0:
                str_list.append(" ")
            str_list.append(f";{self.comment}")

        if self.result and len(self.result) > 0:
            str_list.append(f" => {self.result}")

        return "".join(str_list)

    def short_str(self):
        """Convert only the command portion to a text-based G/M/T-code (e.g. G28)"""
        if self.type == CodeType.Comment:
            return "(comment)"

        prefix = "G53 " if self.is_flag_set(CodeFlags.EnforceAbsolutePosition) else ""
        if self.majorNumber is not None:
            if self.minorNumber is not None:
                return f"{prefix}{self.type}{self.majorNumber}.{self.minorNumber}"

            return f"{prefix}{self.type}{self.majorNumber}"

        return f"{prefix}{self.type}"

    def keyword_to_str(self):
        """Convert the keyword to a string"""
        return {
            KeywordType.If: "if",
            KeywordType.ElseIf: "elif",
            KeywordType.Else: "else",
            KeywordType.While: "while",
            KeywordType.Break: "break",
            KeywordType.Continue: "continue",
            KeywordType.Abort: "abort",
            KeywordType.Var: "var",
            KeywordType.Set: "set",
            KeywordType.Echo: "echo",
            KeywordType.Global: "global",
        }.get(self.keyword)

    def is_flag_set(self, flag: CodeFlags):
        return self.flags & flag != 0