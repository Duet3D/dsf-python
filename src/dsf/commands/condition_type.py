from enum import IntEnum

from ..utils import DeprecatedAliasEnumType


class KeywordType(IntEnum, metaclass=DeprecatedAliasEnumType):
    """Enumeration of conditional G-code keywords"""

    # No conditional code
    NONE = 0

    # If condition
    IF = 1

    # Else-if condition
    ELSE_IF = 2

    # Else condition
    ELSE = 3

    # While condition
    WHILE = 4

    # Break instruction
    BREAK = 5

    # Abort instruction
    ABORT = 6

    # Var operation
    VAR = 7

    # Set operation
    SET = 8

    # Echo operation
    ECHO = 9

    # Continue instruction
    CONTINUE = 10

    # Global operation
    GLOBAL = 11

    # Skip the rest of the current line (no-op)
    SKIP = 12

    # Previous names, deprecated
    Abort = ABORT
    Break = BREAK
    Continue = CONTINUE
    Echo = ECHO
    Else = ELSE
    ElseIf = ELSE_IF
    Global = GLOBAL
    If = IF
    KeywordNone = NONE
    Set = SET
    Skip = SKIP
    Var = VAR
    While = WHILE
