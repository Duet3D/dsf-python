from enum import Enum


class MachineStatus(str, Enum):
    """Possible states of the firmware"""

    # Not connected to the Duet
    disconnected = "disconnected"

    # Processing config.g
    starting = "starting"

    # The firmware is being updated
    updating = "updating"

    # The machine is turned off (i.e. the input voltage is too low for operation)
    off = "off"

    # The machine has encountered an emergency stop and is ready to reset
    halted = "halted"

    # The machine is about to pause a file job
    pausing = "pausing"

    # The machine has paused a file job
    paused = "paused"

    # The machine is about to resume a paused file job
    resuming = "resuming"

    # Job file is being cancelled
    cancelling = "cancelling"

    # The machine is processing a file job
    processing = "processing"

    # The machine is simulating a file job to determine its processing time
    simulating = "processing"

    # The machine is busy doing something (e.g. moving)
    busy = "busy"

    # The machine is changing the current tool
    changingTool = "changingTool"

    # The machine is on but has nothing to do
    idle = "idle"
