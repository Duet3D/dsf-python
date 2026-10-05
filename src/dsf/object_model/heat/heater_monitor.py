from enum import Enum, IntEnum

from ...utils import DeprecatedAliasEnumType
from ..model_object import ModelObject
from ..utils import model_prop, nullable_model_prop


class HeaterMonitorAction(IntEnum, metaclass=DeprecatedAliasEnumType):
    """Action to take when a heater monitor is triggered"""

    # Generate a heater fault
    GENERATE_FAULT = 0

    # Permanently switch off the heater
    PERMANENT_SWITCH_OFF = 1

    # Temporarily switch off the heater until the condition is no longer met
    TEMPORARY_SWITCH_OFF = 2

    # Shut down the printer
    SHUT_DOWN = 3

    # Previous names, deprecated
    generateFault = GENERATE_FAULT
    permanentSwitchOff = PERMANENT_SWITCH_OFF
    shutDown = SHUT_DOWN
    temporarySwitchOff = TEMPORARY_SWITCH_OFF


class HeaterMonitorCondition(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Trigger condition for a heater monitor"""

    # Heater monitor is disabled
    DISABLED = "disabled"

    # Limit temperature has been exceeded
    TOO_HIGH = "tooHigh"

    # Limit temperature is too low
    TOO_LOW = "tooLow"

    # Previous names, deprecated
    disabled = DISABLED
    tooHigh = TOO_HIGH
    tooLow = TOO_LOW


class HeaterMonitor(ModelObject):
    """Information about a heater monitor"""

    # Action to perform when the trigger condition is met
    action = nullable_model_prop("action", HeaterMonitorAction, lambda: None)

    # Condition to meet to perform an action
    condition = model_prop("condition", HeaterMonitorCondition, HeaterMonitorCondition.DISABLED)

    # Limit threshold for this heater monitor
    limit = nullable_model_prop("limit", float)

    # Sensor number to monitor
    sensor = model_prop("sensor", int, -1)

    def __init__(self):
        super().__init__()
