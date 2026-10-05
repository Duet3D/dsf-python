import json
import warnings
from typing import Any, Generic, Optional, Self, TypeVar, cast, overload

from .base_command import BaseCommand
from .code_channel import CodeChannel
from .code_flags import CodeFlags
from .code_parameter import CodeParameter
from .code_type import CodeType
from .condition_type import KeywordType
from ..object_model.messages import Message
from ..utils import DeprecatedWarning, JSONObj, get_typed_value

T = TypeVar("T")


def _get(data: JSONObj, key: str, expected_type: Any, default: T) -> T:
    """Get a typed value from a JSON dictionary or the default value if it is missing or null"""
    return cast(T, get_typed_value(data, key, expected_type)) if data.get(key) is not None else default


class _DeprecatedAlias(Generic[T]):
    """camelCase alias of a Code attribute, kept for backwards compatibility"""

    def __init__(self, name: str) -> None:
        self._name = name

    def __set_name__(self, owner: type, alias: str) -> None:
        self._alias = alias

    def _warn(self) -> None:
        warnings.warn(
            f"Code.{self._alias} is deprecated, use Code.{self._name} instead", DeprecatedWarning, stacklevel=3
        )

    @overload
    def __get__(self, obj: None, objtype: Optional[type] = None) -> Self: ...

    @overload
    def __get__(self, obj: object, objtype: Optional[type] = None) -> T: ...

    def __get__(self, obj: Optional[object], objtype: Optional[type] = None) -> Self | T:
        if obj is None:
            return self
        self._warn()
        return cast(T, getattr(obj, self._name))

    def __set__(self, obj: object, value: T) -> None:
        self._warn()
        setattr(obj, self._name, value)


class Code(BaseCommand):
    """A parsed representation of a generic G/M/T-code"""

    @classmethod
    def from_json(cls, data: JSONObj) -> "Code":
        """Deserialize an instance of this class from JSON deserialized dictionary"""
        result: Optional[JSONObj] = _get(data, "result", dict[str, Any], None)
        parameters: list[JSONObj] = _get(data, "parameters", list[dict[str, Any]], [])
        return cls(
            source_connection=_get(data, "sourceConnection", int, 0),
            result=None if result is None else Message.from_json(result),
            type=CodeType(_get(data, "type", str, CodeType.CodeNone)),
            channel=CodeChannel(_get(data, "channel", str, CodeChannel.DEFAULT_CHANNEL)),
            line_number=_get(data, "lineNumber", int, None),
            indent=_get(data, "indent", int, 0),
            keyword=KeywordType(_get(data, "keyword", int, KeywordType.KeywordNone)),
            keyword_argument=_get(data, "keywordArgument", str, None),
            major_number=_get(data, "majorNumber", int, None),
            minor_number=_get(data, "minorNumber", int, -1),
            flags=CodeFlags(_get(data, "flags", int, CodeFlags.CodeFlagsNone)),
            comment=_get(data, "comment", str, None),
            file_position=_get(data, "filePosition", int, None),
            length=_get(data, "length", int, None),
            parameters=[CodeParameter.from_json(parameter) for parameter in parameters],
        )

    def __init__(
        self,
        type: CodeType = CodeType.CodeNone,
        major_number: Optional[int] = None,
        minor_number: int = -1,
        parameters: Optional[list[CodeParameter]] = None,
        channel: CodeChannel = CodeChannel.DEFAULT_CHANNEL,
        keyword: KeywordType = KeywordType.KeywordNone,
        keyword_argument: Optional[str] = None,
        flags: CodeFlags = CodeFlags.CodeFlagsNone,
        comment: Optional[str] = None,
        line_number: Optional[int] = None,
        indent: int = 0,
        file_position: Optional[int] = None,
        length: Optional[int] = None,
        source_connection: int = 0,
        result: Optional[Message] = None,
    ) -> None:
        super().__init__("Code")

        # The connection ID this code was received from. If this is 0, the code originates from an internal DCS task
        # Usually there is no need to populate this property.
        # It is internally overwritten by the control server on receipt
        self.source_connection = source_connection

        # Result of this code. This property is only set when the code has finished its execution.
        # It remains None if the code has been cancelled
        self.result = result

        # Type of the code
        self.type = type

        # Code channel to send this code to
        self.channel = channel

        # Line number of this code
        self.line_number = line_number

        # Number of whitespaces prefixing the command content
        self.indent = indent

        # Type of conditional G-code (if any)
        self.keyword = keyword

        # Argument of the conditional G-code (if any)
        self.keyword_argument = keyword_argument

        # Major code number (e.g. 28 in G28)
        self.major_number = major_number

        # Minor code number (e.g. 3 in G54.3) or -1 if there is none
        self.minor_number = minor_number

        # Flags of this code
        self.flags = flags

        # Comment of the G/M/T-code. May be null if no comment is present
        # The parser combines different comment segments and concatenates them as a single value.
        # So for example a code like 'G28 (Do homing) ; via G28'
        # causes the Comment field to be filled with 'Do homing via G28'
        self.comment = comment

        # File position of this code in bytes (optional)
        self.file_position = file_position

        # Length of the original code in bytes (optional)
        self.length = length

        # List of parsed code parameters
        self.parameters: list[CodeParameter] = [] if parameters is None else parameters

    sourceConnection = _DeprecatedAlias[int]("source_connection")
    lineNumber = _DeprecatedAlias[Optional[int]]("line_number")
    keywordArgument = _DeprecatedAlias[Optional[str]]("keyword_argument")
    majorNumber = _DeprecatedAlias[Optional[int]]("major_number")
    minorNumber = _DeprecatedAlias[int]("minor_number")
    filePosition = _DeprecatedAlias[Optional[int]]("file_position")

    @property
    def explicit_line_number(self) -> Optional[int]:
        """Line number of this code if it was specified explicitly (N parameter)"""
        return self.line_number if self.is_flag_set(CodeFlags.HasExplicitLineNumber) else None

    @property
    def is_from_file_channel(self) -> bool:
        """Check if this code is from a file channel"""
        return self.channel is CodeChannel.File or self.channel is CodeChannel.File2

    def to_dict(self) -> JSONObj:
        """Convert this code to a JSON dictionary in the format DSF reads it"""
        return {
            "command": self.command,
            "sourceConnection": self.source_connection,
            "result": None if self.result is None else json.loads(self.result.to_json()),
            "type": self.type,
            "channel": self.channel,
            "lineNumber": self.line_number,
            "explicitLineNumber": self.explicit_line_number,
            "indent": self.indent,
            "keyword": self.keyword,
            "keywordArgument": self.keyword_argument,
            "majorNumber": self.major_number,
            "minorNumber": self.minor_number,
            "flags": self.flags,
            "comment": self.comment,
            "filePosition": self.file_position,
            "length": self.length,
            "parameters": [parameter.to_dict() for parameter in self.parameters],
        }

    def to_json(self) -> str:
        """Serialize this code to JSON in the format DSF reads it"""
        return json.dumps(self.to_dict())

    @overload
    def parameter(self, letter: str, default: None = None) -> Optional[CodeParameter]: ...  # type: ignore[misc]

    @overload
    def parameter(self, letter: str, default: object) -> CodeParameter: ...

    def parameter(self, letter: str, default: Optional[object] = None) -> Optional[CodeParameter]:
        """Retrieve the parameter whose letter equals c or generate a default parameter"""
        letter = letter.upper()
        param = [param for param in self.parameters if param.letter.upper() == letter]
        if len(param) > 0:
            return param[0]
        if default is not None:
            return CodeParameter.simple_param(letter, default)
        return None

    def get_unprecedented_string(self, quote: bool = False) -> str:
        """
        Reconstruct an unprecedented string from the parameter list or
        retrieve the parameter which does not have a letter assigned.
        """
        str_list: list[str] = []
        for param in self.parameters:
            if quote and param.is_string:
                str_list.append(f'{param.letter}"{param.string_value}"')
            else:
                str_list.append(f"{param.letter}{param.string_value}")
        return " ".join(str_list)

    def __str__(self) -> str:
        """Convert the parsed code back to a text-based G/M/T-code"""
        if self.keyword != KeywordType.KeywordNone:
            text = self.keyword_to_str() or ""
            if self.keyword_argument is not None:
                text += f" {self.keyword_argument}"
        elif self.type == CodeType.Comment:
            return f";{self.comment}"
        else:
            str_list = [self.short_str()]
            str_list.extend(str(param) for param in self.parameters)
            if self.comment:
                str_list.append(f";{self.comment}")
            text = " ".join(item for item in str_list if item)

        if self.result is not None and self.result.content:
            text += f" => {self.result!r}".rstrip()
        return text

    def short_str(self) -> str:
        """Convert only the command portion to a text-based G/M/T-code (e.g. G28)"""
        if self.keyword != KeywordType.KeywordNone:
            return self.keyword_to_str() or ""

        if self.type == CodeType.CodeNone:
            return ""

        if self.type == CodeType.Comment:
            return "(comment)"

        code_type = CodeType(self.type).value
        prefix = "G53 " if self.is_flag_set(CodeFlags.EnforceAbsolutePosition) else ""
        if self.major_number is not None:
            if self.minor_number >= 0:
                return f"{prefix}{code_type}{self.major_number}.{self.minor_number}"

            return f"{prefix}{code_type}{self.major_number}"

        return f"{prefix}{code_type}"

    def keyword_to_str(self) -> Optional[str]:
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
            KeywordType.Skip: "skip",
        }.get(self.keyword)

    def is_flag_set(self, flag: CodeFlags) -> bool:
        return self.flags & flag != 0
