from enum import Enum


class ToolState(str, Enum):
    """States of a tool"""

    # Tool is turned off
    off = "off"

    # Tool is active
    active = "active"

    # Tool is in standby
    standby = "standby"
