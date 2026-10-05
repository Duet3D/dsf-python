from enum import Enum

from ..utils import DeprecatedAliasEnumType


class CodeType(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Type of generic G/M/T-code. If none is applicable, it is treated as a comment"""

    # Undetermined
    NONE = ""

    # Whole line comment
    COMMENT = "Q"

    # Meta G-code keyword (not sent as a code to RRF)
    # Codes of this type are not sent to RRF in binary representation
    KEYWORD = "K"

    # G-code
    GCODE = "G"

    # M-code
    MCODE = "M"

    # T-code
    TCODE = "T"

    # Previous names, deprecated
    CodeNone = NONE
    Comment = COMMENT
    GCode = GCODE
    Keyword = KEYWORD
    MCode = MCODE
    TCode = TCODE
