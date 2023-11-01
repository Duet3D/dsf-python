from enum import Enum


class CodeType(str, Enum):
    """Type of generic G/M/T-code. If none is applicable, it is treated as a comment"""

    # Undetermined
    CodeNone = "\0"

    # Whole line comment
    Comment = "Q"

    # Meta G-code keyword (not sent as a code to RRF)
    # Codes of this type are not sent to RRF in binary representation
    Keyword = "K"

    # G-code
    GCode = "G"

    # M-code
    MCode = "M"

    # T-code
    TCode = "T"
