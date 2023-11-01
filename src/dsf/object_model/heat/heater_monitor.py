from __future__ import annotations
from enum import Enum, IntEnum

from ..model_object import ModelObject


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

    def __init__(self):
        super().__init__()
        # Action to perform when the trigger condition is met
        self._action = HeaterMonitorAction.generateFault
        # Condition to meet to perform an action
        self._condition = HeaterMonitorCondition.disabled
        # Limit threshold for this heater monitor
        self._limit = None

    @property
    def action(self) -> HeaterMonitorAction | None:
        """Action to perform when the trigger condition is met"""
        return self._action

    @action.setter
    def action(self, value: HeaterMonitorAction | None = None):
        if value is None or isinstance(value, HeaterMonitorAction):
            self._action = value
        elif isinstance(value, int):
            self._action = HeaterMonitorAction(value)
        else:
            raise TypeError(f"{__name__}.action must be of type HeaterMonitorAction or None."
                            f" Got {type(value)}: {value}")

    @property
    def condition(self):
        """Condition to meet to perform an action"""
        return self._condition

    @condition.setter
    def condition(self, value: HeaterMonitorCondition = HeaterMonitorCondition.disabled):
        if isinstance(value, HeaterMonitorCondition):
            self._condition = value
        elif isinstance(value, str):
            self._condition = HeaterMonitorCondition(value)
        else:
            raise TypeError(f"{__name__}.condition must be of type HeaterMonitorCondition or None."
                            f" Got {type(value)}: {value}")

    @property
    def limit(self) -> float | None:
        """Limit threshold for this heater monitor"""
        return self._limit

    @limit.setter
    def limit(self, value: float | None = None):
        self._limit = float(value) if value is not None else None
