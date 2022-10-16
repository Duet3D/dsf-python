from enum import Enum


class InputChannelState(str, Enum):
    """State of a channel"""

    # Awaiting message acknowledgement
    awaitingAcknowledgement = "awaitingAcknowledgement"

    # Channel is idle
    idle = "idle"

    # Channel is executing a G/M/T-code
    executing = "executing"

    # Channel is waiting for more data
    waiting = "waiting"

    # Channel is reading a G/M/T-code
    reading = "reading"
