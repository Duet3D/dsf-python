"""
codeparameter contains all classes and methods dealing with deserialized code parameters.
"""
import json

from ..exceptions import CodeParserException
from ..utility.driver_id import DriverId


class CodeParameter(json.JSONEncoder):
    """Represents a parsed parameter of a G/M/T-code"""

    LETTER_FOR_UNPRECEDENTED_STRING = "@"

    def default(self, o):
        return {
            "letter": o.letter,
            "value": o.value,
            "isString": isinstance(o.value, str),
            "isDriverId": o.is_driver_id,
        }

    @classmethod
    def from_json(cls, data):
        """Instantiate a new instance of this class from JSON deserialized dictionary"""
        return cls(**data)

    @classmethod
    def simple_param(cls, letter: str, value, isDriverId: bool = False):
        """Create a new simple parameter without parsing the value"""
        return cls(letter, value, isDriverId=isDriverId)

    def __init__(self, letter: str, value, isString: bool = None, isDriverId: bool = None):
        """
        Creates a new CodeParameter instance and parses value to a native data type
        if applicable
        """

        # This is the simple path to create a CodeParameter
        if isString is None and isDriverId is None:
            self.letter = letter
            self.string_value = str(value)
            self.__parsed_value = value
            self.is_expression = self.string_value.startswith("{}") and self.string_value.endswith("}")
            return

        self.letter = letter
        self.string_value = value
        self.is_string = isString
        self.is_expression = False
        self.is_driver_id = isDriverId if isDriverId is not None else False
        if self.is_string:
            self.__parsed_value = value
            return
        elif self.is_driver_id:
            drivers = [DriverId(as_str=value) for value in self.string_value.split(":")]
            self.__parsed_value = drivers[0] if len(drivers) == 1 else drivers

        value = value.strip()
        # Empty parameters are represented as integers with the value 0 (e.g. G92 XY => G92 X0 Y0)
        if not value:
            self.__parsed_value = 0
        elif value.startswith("{}") and value.endswith("}"):  # It is an expression
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

    def convert_driver_ids(self):
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

        drivers = []
        parameters = self.string_value.split(":")
        for value in parameters:
            segments = value.split(".")
            segment_count = len(segments)
            if segment_count == 1:
                drivers.append(int(segments[0]))
            elif segment_count == 2:
                driver = (int(segments[0]) << 16) & 0xFFFF
                driver |= int(segments[1] & 0xFFFF)
            else:
                raise CodeParserException(f"Driver value from {self.letter} parameter is invalid")

        self.__parsed_value = drivers[0] if len(drivers) == 1 else drivers
        self.is_driver_id = True

    def as_float(self):
        """Conversion to float"""
        if isinstance(self.__parsed_value, float):
            return self.__parsed_value
        if isinstance(self.__parsed_value, int):
            return float(self.__parsed_value)

        raise Exception(f"Cannot convert {self.letter} parameter to float (value {self.string_value})")

    def as_int(self):
        """Conversion to int"""
        if isinstance(self.__parsed_value, int):
            return self.__parsed_value
        if isinstance(self.__parsed_value, DriverId):
            return self.__parsed_value.as_int()

        raise Exception(f"Cannot convert {self.letter} parameter to int (value {self.string_value})")

    def as_driver_id(self):
        if isinstance(self.__parsed_value, DriverId):
            return self.__parsed_value
        if isinstance(self.__parsed_value, int):
            try:
                return DriverId(as_int=self.__parsed_value)
            except:  # noqa
                pass
        raise Exception(f"Cannot convert {self.letter} parameter to DriverId (value {self.string_value})")

    def as_float_array(self):
        """Conversion to float array"""
        try:
            if isinstance(self.__parsed_value, list):
                return list(map(float, self.__parsed_value))
            if isinstance(self.__parsed_value, float):
                return [self.__parsed_value]
            if isinstance(self.__parsed_value, int):
                return [float(self.__parsed_value)]
        except:  # noqa
            pass
        raise Exception(f"Cannot convert {self.letter} parameter to float array (value {self.string_value})")

    def as_int_array(self):
        """Conversion to int array"""
        try:
            if isinstance(self.__parsed_value, list):
                if isinstance(self.__parsed_value[0], DriverId):
                    return [d.as_int() for d in self.__parsed_value]
                return list(map(int, self.__parsed_value))
            if isinstance(self.__parsed_value, int):
                return [self.__parsed_value]
            if isinstance(self.__parsed_value, DriverId):
                return [self.__parsed_value.as_int()]
        except:  # noqa
            pass
        raise Exception(f"Cannot convert {self.letter} parameter to float array (value {self.string_value})")

    def as_driver_id_array(self):
        try:
            if isinstance(self.__parsed_value, list):
                if isinstance(self.__parsed_value[0], DriverId):
                    return self.__parsed_value
                if isinstance(self.__parsed_value[0], int):
                    return list(map(DriverId, self.__parsed_value))
            if isinstance(self.__parsed_value, DriverId):
                return [self.__parsed_value]
            if isinstance(self.__parsed_value, int):
                return [DriverId(as_int=self.__parsed_value)]
        except:  # noqa
            pass
        raise Exception(f"Cannot convert {self.letter} parameter to DriverId array (value {self.string_value})")

    def as_bool(self):
        """Conversion to bool"""
        try:
            return float(self.string_value) > 0
        except:  # noqa
            return False

    def __eq__(self, other):
        if self is None:
            return other is None
        if isinstance(other, CodeParameter):
            return self.letter == other.letter and self.__parsed_value == other.__parsed_value
        return self.__parsed_value == other

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        letter = self.letter if not self.letter == CodeParameter.LETTER_FOR_UNPRECEDENTED_STRING else ""
        if self.is_string and not self.is_expression:
            double_quoted = self.string_value.replace('"', '""')
            return f'{letter}"{double_quoted}"'

        return f"{letter}{self.string_value}"
