"""
codeparameter contains all classes and methods dealing with deserialized code parameters.
"""
import json
from typing import cast

from ..exceptions import CodeParserException
from ..object_model.move.driver_id import DriverId


ParsedValue = str | int | float | DriverId | list[int] | list[float] | list[DriverId]


class CodeParameter(json.JSONEncoder):
    """Represents a parsed parameter of a G/M/T-code"""

    LETTER_FOR_UNPRECEDENTED_STRING = "@"

    letter: str
    string_value: str
    is_string: bool
    is_expression: bool
    is_driver_id: bool
    __parsed_value: ParsedValue

    def default(self, o: object) -> dict[str, object]:
        if not isinstance(o, CodeParameter):
            return super().default(o)
        return {
            "letter": o.letter,
            "value": o.value,
            "isString": isinstance(o.value, str),
            "isDriverId": o.is_driver_id,
        }

    @classmethod
    def from_json(cls, data: dict[str, object]) -> "CodeParameter":
        """Instantiate a new instance of this class from JSON deserialized dictionary"""
        letter = str(data["letter"])
        value = data.get("value", "")
        is_string = data.get("isString")
        is_driver_id = data.get("isDriverId")
        return cls(
            letter,
            value,
            isString=is_string if isinstance(is_string, bool) else None,
            isDriverId=is_driver_id if isinstance(is_driver_id, bool) else None,
        )

    @classmethod
    def simple_param(cls, letter: str, value: object, isDriverId: bool = False) -> "CodeParameter":
        """Create a new simple parameter without parsing the value"""
        return cls(letter, value, isDriverId=isDriverId)

    def __init__(
        self,
        letter: str,
        value: object,
        isString: bool | None = None,
        isDriverId: bool | None = None,
    ) -> None:
        """
        Creates a new CodeParameter instance and parses value to a native data type
        if applicable
        """

        # This is the simple path to create a CodeParameter
        if isString is None and isDriverId is None:
            self.letter = letter
            self.string_value = str(value)
            if isinstance(value, (str, int, float, DriverId)):
                self.__parsed_value = value
            elif isinstance(value, list):
                list_value = cast(list[object], value)
                if all(isinstance(item, (int, float, DriverId)) for item in list_value):
                    self.__parsed_value = cast(ParsedValue, list_value)
                else:
                    self.__parsed_value = self.string_value
            else:
                self.__parsed_value = self.string_value
            self.is_expression = self.string_value.startswith("{") and self.string_value.endswith("}")
            self.is_string = isinstance(self.__parsed_value, str)
            self.is_driver_id = isinstance(self.__parsed_value, DriverId) or (
                isinstance(self.__parsed_value, list)
                and all(isinstance(item, DriverId) for item in self.__parsed_value)
            )
            return

        self.letter = letter
        self.string_value = str(value)
        self.is_string = bool(isString)
        self.is_expression = False
        self.is_driver_id = isDriverId if isDriverId is not None else False
        if self.is_string:
            self.__parsed_value = self.string_value
            return
        elif self.is_driver_id:
            drivers = [DriverId(as_str=driver_value) for driver_value in self.string_value.split(":")]
            self.__parsed_value = drivers[0] if len(drivers) == 1 else drivers
            return

        parsed_text = self.string_value.strip()
        # Empty parameters are represented as integers with the value 0 (e.g. G92 XY => G92 X0 Y0)
        if not parsed_text:
            self.__parsed_value = 0
        elif parsed_text.startswith("{") and parsed_text.endswith("}"):  # It is an expression
            self.is_expression = True
            self.__parsed_value = parsed_text
        elif ":" in parsed_text:  # It is an array (or a string)
            split = parsed_text.split(":")
            try:
                if "." in parsed_text:  # If there is a dot anywhere, attempt to parse it as a float array
                    self.__parsed_value = list(map(float, split))
                else:  # If there is no dot, it could be an integer array
                    self.__parsed_value = list(map(int, split))
            except:  # noqa
                self.__parsed_value = parsed_text
        else:
            try:
                self.__parsed_value = int(parsed_text)
            except:  # noqa
                try:
                    self.__parsed_value = float(parsed_text)
                except:  # noqa
                    self.__parsed_value = parsed_text

    @property
    def value(self) -> ParsedValue:
        return self.__parsed_value

    def convert_driver_ids(self) -> None:
        """Convert this parameter to driver id(s)"""
        if self.is_expression:
            return
        if not isinstance(self.__parsed_value, str):
            self.is_driver_id = True
            return
        try:
            driver_ids = [DriverId(as_str=value) for value in self.string_value.split(":")]
        except CodeParserException as e:
            raise CodeParserException(f"{e} from {self.letter} parameter")

        if len(driver_ids) == 1:
            self.__parsed_value = driver_ids[0]
        else:
            self.__parsed_value = driver_ids

        drivers: list[int] = []
        parameters = self.string_value.split(":")
        for value in parameters:
            segments = value.split(".")
            segment_count = len(segments)
            if segment_count == 1:
                drivers.append(int(segments[0]))
            elif segment_count == 2:
                driver = (int(segments[0]) << 16) & 0xFFFF
                driver |= int(segments[1]) & 0xFFFF
                drivers.append(driver)
            else:
                raise CodeParserException(f"Driver value from {self.letter} parameter is invalid")

        self.__parsed_value = drivers[0] if len(drivers) == 1 else drivers
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
            return self.__parsed_value.as_int()

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

    def as_float_array(self) -> list[float]:
        """Conversion to float array"""
        try:
            if isinstance(self.__parsed_value, list):
                parsed_values = cast(list[object], self.__parsed_value)
                if all(isinstance(value, (int, float)) for value in parsed_values):
                    numeric_values = cast(list[int | float], parsed_values)
                    return [float(value) for value in numeric_values]
            if isinstance(self.__parsed_value, float):
                return [self.__parsed_value]
            if isinstance(self.__parsed_value, int):
                return [float(self.__parsed_value)]
        except:  # noqa
            pass
        raise Exception(f"Cannot convert {self.letter} parameter to float array (value {self.string_value})")

    def as_int_array(self) -> list[int]:
        """Conversion to int array"""
        try:
            if isinstance(self.__parsed_value, list):
                if not self.__parsed_value:
                    return []
                parsed_values = cast(list[object], self.__parsed_value)
                if all(isinstance(value, DriverId) for value in parsed_values):
                    driver_values = cast(list[DriverId], parsed_values)
                    return [driver.as_int() for driver in driver_values]
                if all(isinstance(value, (int, float)) for value in parsed_values):
                    numeric_values = cast(list[int | float], parsed_values)
                    return [int(value) for value in numeric_values]
            if isinstance(self.__parsed_value, int):
                return [self.__parsed_value]
            if isinstance(self.__parsed_value, DriverId):
                return [self.__parsed_value.as_int()]
        except:  # noqa
            pass
        raise Exception(f"Cannot convert {self.letter} parameter to float array (value {self.string_value})")

    def as_driver_id_array(self) -> list[DriverId]:
        try:
            if isinstance(self.__parsed_value, list):
                if not self.__parsed_value:
                    return []
                if all(isinstance(value, DriverId) for value in self.__parsed_value):
                    return cast(list[DriverId], self.__parsed_value)
                if all(isinstance(value, int) for value in self.__parsed_value):
                    return [DriverId(as_int=value) for value in cast(list[int], self.__parsed_value)]
            if isinstance(self.__parsed_value, DriverId):
                return [self.__parsed_value]
            if isinstance(self.__parsed_value, int):
                return [DriverId(as_int=self.__parsed_value)]
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
        if self.is_string and not self.is_expression:
            double_quoted = self.string_value.replace('"', '""')
            return f'{letter}"{double_quoted}"'

        return f"{letter}{self.string_value}"
