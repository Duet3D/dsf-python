from enum import Enum

from ...utils import DeprecatedAliasEnumType


class InputChannelState(str, Enum, metaclass=DeprecatedAliasEnumType):
    """State of a channel"""

    # Awaiting message acknowledgement
    AWAITING_ACKNOWLEDGEMENT = "awaitingAcknowledgement"

    # Channel is idle
    IDLE = "idle"

    # Channel is executing a G/M/T-code
    EXECUTING = "executing"

    # Channel is waiting for more data
    WAITING = "waiting"

    # Channel is reading a G/M/T-code
    READING = "reading"

    # Channel is unused
    UNUSED = "unused"

    # Previous names, deprecated
    awaitingAcknowledgement = AWAITING_ACKNOWLEDGEMENT
    executing = EXECUTING
    idle = IDLE
    reading = READING
    unused = UNUSED
    waiting = WAITING
