"""
codeparameter contains all classes and methods dealing with deserialized code parameters.
"""

from typing import Optional, Self, TypeAlias, cast

from ..exceptions import CodeParserException
from ..object_model.move.driver_id import DriverId
from ..utils import JSONObj, get_typed_value

CodeParameterScalar: TypeAlias = str | int | float | DriverId
CodeParameterArray: TypeAlias = list[int] | list[float] | list[DriverId]
CodeParameterValue: TypeAlias = CodeParameterScalar | CodeParameterArray


def _to_string_value(value: object) -> str:
    """Convert a parameter value to its G-code representation (arrays are separated by colons)"""
    if value is None:
        return ""
    if isinstance(value, list):
        return ":".join(str(item) for item in cast(list[object], value))
    return str(value)


class CodeParameter:
    """Represents a parsed parameter of a G/M/T-code"""

    LETTER_FOR_UNPRECEDENTED_STRING = "@"
    letter: str
    string_value: str
    is_string: bool
    is_expression: bool
    is_driver_id: bool
    __parsed_value: object

    @property
    def value(self) -> object:
        return self.__parsed_value

    @classmethod
    def from_json(cls, data: JSONObj) -> Self:
        """Instantiate a new instance of this class from JSON deserialized dictionary"""
        return cls(
            get_typed_value(data, "letter", str),
            get_typed_value(data, "value", str),
            isString=get_typed_value(data, "isString", bool) if "isString" in data else False,
            isDriverId=get_typed_value(data, "isDriverId", bool) if "isDriverId" in data else False,
        )

    def to_dict(self) -> JSONObj:
        """Convert this parameter to a JSON dictionary in the format DSF reads it"""
        data: JSONObj = {"letter": self.letter, "value": self.string_value}
        if self.is_driver_id:
            data["isDriverId"] = True
        data["isString"] = self._is_string_value()
        return data

    def _is_string_value(self) -> bool:
        """Check if the parsed value is a string that must be quoted, like DSF does"""
        return isinstance(self.__parsed_value, str) and not self.is_expression

    @classmethod
    def simple_param(cls, letter: str, value: object, isDriverId: bool = False) -> Self:
        """Create a new simple parameter without parsing the value"""
        return cls(letter, value, isDriverId=isDriverId)

    def __init__(
        self,
        letter: str,
        value: object,
        isString: Optional[bool] = None,
        isDriverId: Optional[bool] = None,
    ) -> None:
        """
        Creates a new CodeParameter instance and parses value to a native data type
        if applicable
        """

        # This is the simple path to create a CodeParameter
        if isString is None and isDriverId is None:
            self.letter = letter
            self.string_value = _to_string_value(value)
            self.__parsed_value = value
            self.is_expression = self.string_value.startswith("{") and self.string_value.endswith("}")
            self.is_string = isinstance(value, str) and not self.is_expression
            items = cast(list[object], value) if isinstance(value, list) else [value]
            self.is_driver_id = len(items) > 0 and all(isinstance(item, DriverId) for item in items)
            return

        self.letter = letter
        self.string_value = _to_string_value(value)
        self.is_string = bool(isString)
        self.is_expression = False
        self.is_driver_id = isDriverId if isDriverId is not None else False
        if self.is_string:
            self.__parsed_value = value
            return
        elif self.is_driver_id:
            drivers = [DriverId(as_str=driver_value) for driver_value in self.string_value.split(":")]
            self.__parsed_value = drivers[0] if len(drivers) == 1 else drivers
            return

        value = self.string_value.strip()
        # Empty parameters are represented as integers with the value 0 (e.g. G92 XY => G92 X0 Y0)
        if not value:
            self.__parsed_value = 0
        elif value.startswith("{") and value.endswith("}"):  # It is an expression
            self.is_expression = True
            self.__parsed_value = value
        elif ":" in value:  # It is an array (or a string)
            split = value.split(":")
            try:
                if "." in value:  # If there is a dot anywhere, attempt to parse it as a float array
                    self.__parsed_value = list(map(float, split))
                else:  # If there is no dot, it could be an integer array
                    self.__parsed_value = list(map(int, split))
            except:  # noqa
                self.__parsed_value = value
        else:
            try:
                self.__parsed_value = int(value)
            except:  # noqa
                try:
                    self.__parsed_value = float(value)
                except:  # noqa
                    self.__parsed_value = value

    def convert_driver_ids(self) -> None:
        """Convert this parameter to driver id(s)"""
        if self.is_expression:
            return
        try:
            drivers = [DriverId(as_str=value) for value in self.string_value.split(":")]
        except CodeParserException as e:
            raise CodeParserException(f"{e} from {self.letter} parameter")

        if len(drivers) == 1:
            self.__parsed_value = drivers[0]
        else:
            self.__parsed_value = drivers

        self.is_driver_id = True

    def as_float(self) -> float:
        """Conversion to float"""
        if isinstance(self.__parsed_value, float):
            return self.__parsed_value
        if isinstance(self.__parsed_value, int):
            return float(self.__parsed_value)

        raise Exception(f"Cannot convert {self.letter} parameter to float (value {self.string_value})")

    def as_int(self) -> int:
        """Conversion to int"""
        if isinstance(self.__parsed_value, int):
            return self.__parsed_value
        if isinstance(self.__parsed_value, DriverId):
            return int(self.__parsed_value.as_int())

        raise Exception(f"Cannot convert {self.letter} parameter to int (value {self.string_value})")

    def as_driver_id(self) -> DriverId:
        if isinstance(self.__parsed_value, DriverId):
            return self.__parsed_value
        if isinstance(self.__parsed_value, int):
            try:
                return DriverId(as_int=self.__parsed_value)
            except:  # noqa
                pass
        raise Exception(f"Cannot convert {self.letter} parameter to DriverId (value {self.string_value})")

    def _parse_expression_array(self) -> list[float]:
        """Parse expression-based arrays like {0, 255, 128} into a list of floats."""
        if not self.is_expression:
            raise Exception(
                f"Cannot parse expression array: {self.letter} is not an expression (value {self.string_value})"
            )
        # Strip braces and split by comma
        content = self.string_value[1:-1].strip()  # Remove { }
        if not content:
            return []
        elements = [elem.strip() for elem in content.split(",")]
        try:
            # Try to parse as floats first, then convert to ints if needed
            return [float(elem) for elem in elements if elem]
        except ValueError as e:
            raise Exception(
                f"Cannot parse expression array: failed to convert elements to numbers in {self.letter}"
                f" (value {self.string_value})"
            ) from e

    def as_float_array(self) -> list[float]:
        """Conversion to float array. Supports colon-separated (C0.5:1.0) and expression formats (C{0.5, 1.0})."""
        try:
            parsed_value: object = self.__parsed_value
            if isinstance(parsed_value, list):
                values = cast(list[int | float], parsed_value)
                return [float(value) for value in values]
            if isinstance(parsed_value, float):
                return [parsed_value]
            if isinstance(parsed_value, int):
                return [float(parsed_value)]
            if self.is_expression:
                return self._parse_expression_array()
        except:  # noqa
            pass
        raise Exception(f"Cannot convert {self.letter} parameter to float array (value {self.string_value})")

    def as_int_array(self) -> list[int]:
        """Conversion to int array. Supports colon-separated (C0:255:128) and expression formats (C{0, 255, 128})."""
        try:
            parsed_value: object = self.__parsed_value
            if isinstance(parsed_value, list):
                if isinstance(parsed_value[0], DriverId):
                    driver_ids = cast(list[DriverId], parsed_value)
                    return [int(driver_id.as_int()) for driver_id in driver_ids]
                numbers = cast(list[int] | list[float], parsed_value)
                return [int(value) for value in numbers]
            if isinstance(parsed_value, int):
                return [parsed_value]
            if isinstance(parsed_value, DriverId):
                return [int(parsed_value.as_int())]
            if self.is_expression:
                float_array = self._parse_expression_array()
                return [int(value) for value in float_array]
        except:  # noqa
            pass
        raise Exception(f"Cannot convert {self.letter} parameter to int array (value {self.string_value})")

    def as_driver_id_array(self) -> list[DriverId]:
        try:
            parsed_value: object = self.__parsed_value
            if isinstance(parsed_value, list):
                if isinstance(parsed_value[0], DriverId):
                    return cast(list[DriverId], parsed_value)
                if isinstance(parsed_value[0], int):
                    values = cast(list[int], parsed_value)
                    return [DriverId(as_int=value) for value in values]
            if isinstance(parsed_value, DriverId):
                return [parsed_value]
            if isinstance(parsed_value, int):
                return [DriverId(as_int=parsed_value)]
        except:  # noqa
            pass
        raise Exception(f"Cannot convert {self.letter} parameter to DriverId array (value {self.string_value})")

    def as_bool(self) -> bool:
        """Conversion to bool"""
        try:
            return float(self.string_value) > 0
        except:  # noqa
            return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CodeParameter):
            return self.letter == other.letter and self.__parsed_value == other.__parsed_value
        return self.__parsed_value == other

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __str__(self) -> str:
        letter = self.letter if not self.letter == CodeParameter.LETTER_FOR_UNPRECEDENTED_STRING else ""
        if self._is_string_value():
            double_quoted = self.string_value.replace('"', '""')
            return f'{letter}"{double_quoted}"'

        return f"{letter}{self.string_value}"
