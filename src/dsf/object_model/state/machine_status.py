from enum import Enum

from ...utils import DeprecatedAliasEnumType


class MachineStatus(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Possible states of the firmware"""

    # Not connected to the Duet
    DISCONNECTED = "disconnected"

    # Processing config.g
    STARTING = "starting"

    # The firmware is being updated
    UPDATING = "updating"

    # The machine is turned off (i.e. the input voltage is too low for operation)
    OFF = "off"

    # The machine has encountered an emergency stop and is ready to reset
    HALTED = "halted"

    # The machine is about to pause a file job
    PAUSING = "pausing"

    # The machine has paused a file job
    PAUSED = "paused"

    # The machine is about to resume a paused file job
    RESUMING = "resuming"

    # Job file is being cancelled
    CANCELLING = "cancelling"

    # The machine is processing a file job
    PROCESSING = "processing"

    # The machine is simulating a file job to determine its processing time
    SIMULATING = "simulating"

    # The machine is busy doing something (e.g. moving)
    BUSY = "busy"

    # The machine is changing the current tool
    CHANGING_TOOL = "changingTool"

    # The machine is on but has nothing to do
    IDLE = "idle"

    # Previous names, deprecated
    busy = BUSY
    cancelling = CANCELLING
    changingTool = CHANGING_TOOL
    disconnected = DISCONNECTED
    halted = HALTED
    idle = IDLE
    off = OFF
    paused = PAUSED
    pausing = PAUSING
    processing = PROCESSING
    resuming = RESUMING
    simulating = SIMULATING
    starting = STARTING
    updating = UPDATING
