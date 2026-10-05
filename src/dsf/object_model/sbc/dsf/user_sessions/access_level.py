from enum import Enum

from .....utils import DeprecatedAliasEnumType


class AccessLevel(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Defines what a user is allowed to do"""

    # Changes to the system and/or operation are not permitted
    READ_ONLY = "readOnly"

    # Changes to the system and/or operation are permitted
    READ_WRITE = "readWrite"

    # Previous names, deprecated
    readOnly = READ_ONLY
    readWrite = READ_WRITE
