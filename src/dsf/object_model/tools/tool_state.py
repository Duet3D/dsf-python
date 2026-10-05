from enum import Enum

from ...utils import DeprecatedAliasEnumType


class ToolState(str, Enum, metaclass=DeprecatedAliasEnumType):
    """States of a tool"""

    # Tool is turned off
    OFF = "off"

    # Tool is active
    ACTIVE = "active"

    # Tool is in standby
    STANDBY = "standby"

    # Previous names, deprecated
    active = ACTIVE
    off = OFF
    standby = STANDBY
