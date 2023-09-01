from enum import IntEnum


class KeywordType(IntEnum):
    """Enumeration of conditional G-code keywords"""

    # No conditional code
    KeywordNone = 0

    # If condition
    If = 1

    # Else-if condition
    ElseIf = 2

    # Else condition
    Else = 3

    # While condition
    While = 4

    # Break instruction
    Break = 5

    # Abort instruction
    Abort = 6

    # Var operation
    Var = 7

    # Set operation
    Set = 8

    # Echo operation
    Echo = 9

    # Continue instruction
    Continue = 10

    # Global operation
    Global = 11
