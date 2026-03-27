from enum import Enum, IntEnum

from ..model_object import ModelObject
from ..utils import model_prop, nullable_model_prop


class HeaterMonitorAction(IntEnum):
    """Action to take when a heater monitor is triggered"""

    # Generate a heater fault
    generateFault = 0

    # Permanently switch off the heater
    permanentSwitchOff = 1

    # Temporarily switch off the heater until the condition is no longer met
    temporarySwitchOff = 2

    # Shut down the printer
    shutDown = 3


class HeaterMonitorCondition(str, Enum):
    """Trigger condition for a heater monitor"""

    # Heater monitor is disabled
    disabled = "disabled"

    # Limit temperature has been exceeded
    tooHigh = "tooHigh"

    # Limit temperature is too low
    tooLow = "tooLow"


class HeaterMonitor(ModelObject):
    """Information about a heater monitor"""

    # Action to perform when the trigger condition is met
    action = nullable_model_prop("action", HeaterMonitorAction, lambda: None)

    # Condition to meet to perform an action
    condition = model_prop("condition", HeaterMonitorCondition, HeaterMonitorCondition.disabled)

    # Limit threshold for this heater monitor
    limit = nullable_model_prop("limit", float)

    # Sensor number to monitor
    sensor = model_prop("sensor", int, -1)

    def __init__(self):
        super().__init__()
