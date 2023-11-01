from __future__ import annotations
from datetime import datetime

from .beep_request import BeepRequest
from .gp_output_port import GpOutputPort
from .log_level import LogLevel
from .machine_mode import MachineMode
from .machine_status import MachineStatus
from .message_box import MessageBox
from .restore_point import RestorePoint
from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import wrap_model_property


class State(ModelObject):
    """Information about the machine state"""

    # Information about a requested beep or null if none is requested
    beep = wrap_model_property('beep', BeepRequest)
    # Details about a requested message box or null if none is requested
    message_box = wrap_model_property('message_box', MessageBox)

    def __init__(self):
        super(State, self).__init__()
        self._atx_power = None
        self._atx_power_port = None
        self._beep = None
        self._current_tool = -1
        self._deferred_power_down = None
        self._display_message = ""
        self._dsf_version = None
        self._dsf_plugin_support = False
        self._dsf_root_plugin_support = False
        self._gp_out = ModelCollection(GpOutputPort)
        self._laser_pwm = None
        self._log_file = None
        self._log_level = LogLevel.Off
        self._message_box = None
        self._machine_mode = MachineMode.FFF
        self._macro_restarted = False
        self._ms_up_time = 0
        self._next_tool = -1
        self._plugins_started = False
        self._power_fail_script = ""
        self._previous_tool = -1
        self._restore_points = ModelCollection(RestorePoint)
        self._status = MachineStatus.starting
        self._this_input = None
        self._time = None
        self._up_time = 0

    @property
    def atx_power(self) -> bool | None:
        """State of the ATX power pin (if controlled)"""
        return self._atx_power

    @atx_power.setter
    def atx_power(self, value: bool | None = None):
        self._atx_power = bool(value) if value is not None else None

    @property
    def atx_power_port(self) -> str | None:
        """Port of the ATX power pin or null if not assigned"""
        return self._atx_power_port

    @atx_power_port.setter
    def atx_power_port(self, value: str | None = None):
        self._atx_power_port = str(value) if value is not None else None

    @property
    def current_tool(self) -> int:
        """Number of the currently selected tool or -1 if none is selected"""
        return self._current_tool

    @current_tool.setter
    def current_tool(self, value: int):
        self._current_tool = int(value)

    @property
    def deferred_power_down(self) -> bool | None:
        """When provided it normally has value 0 normally and 1 when a deferred power down is pending
        It is only available after power switching has been enabled by M80 or M81"""
        return self._deferred_power_down

    @deferred_power_down.setter
    def deferred_power_down(self, value: bool | None = None):
        self._deferred_power_down = bool(value) if value is not None else None

    @property
    def display_message(self) -> str:
        """Persistent message to display (see M117)"""
        return self._display_message

    @display_message.setter
    def display_message(self, value: str):
        self._display_message = str(value)

    @property
    def dsf_version(self) -> str | None:
        """Version of the Duet Software Framework package
        Obsolete: This field will be removed in favour of a new dsf main key in v3.5"""
        return self._dsf_version

    @dsf_version.setter
    def dsf_version(self, value: str | None = None):
        self._dsf_version = str(value) if value is not None else None

    @property
    def dsf_plugin_support(self) -> bool:
        """Indicates if DSF allows the installation and usage of third-party plugins
        Obsolete: This field will be removed in favour of a new dsf main key in v3.5"""
        return self._dsf_plugin_support

    @dsf_plugin_support.setter
    def dsf_plugin_support(self, value: bool):
        self._dsf_plugin_support = bool(value)

    @property
    def dsf_root_plugin_support(self) -> bool:
        """Indicates if DSF allows the installation and usage of third-party root plugins (potentially dangerous)
        Obsolete: This field will be removed in favour of a new dsf main key in v3.5"""
        return self._dsf_root_plugin_support

    @dsf_root_plugin_support.setter
    def dsf_root_plugin_support(self, value: bool):
        self._dsf_root_plugin_support = bool(value)

    @property
    def gp_out(self) -> list[GpOutputPort]:
        """List of general-purpose output ports"""
        return self._gp_out

    @property
    def laser_pwm(self) -> float | None:
        """Laser PWM of the next commanded move (0..1) or null if not applicable"""
        return self._laser_pwm

    @laser_pwm.setter
    def laser_pwm(self, value: float | None = None):
        self._laser_pwm = float(value) if value is not None else None

    @property
    def log_file(self) -> str | None:
        """Log file being written to or null if logging is disabled"""
        return self._log_file

    @log_file.setter
    def log_file(self, value: str | None = None):
        self._log_file = str(value) if value is not None else None

    @property
    def log_level(self) -> LogLevel:
        """Current log level"""
        return self._log_level

    @log_level.setter
    def log_level(self, value: LogLevel):
        if isinstance(value, LogLevel):
            self._log_level = value
        elif isinstance(value, str):
            self._log_level = LogLevel(value)
        else:
            raise TypeError(f"{__name__}.log_level must be of type LogLevel."
                            f" Got {type(value)}: {value}")

    @property
    def machine_mode(self) -> MachineMode:
        """Current mode of operation"""
        return self._machine_mode

    @machine_mode.setter
    def machine_mode(self, value: MachineMode):
        if isinstance(value, MachineMode):
            self._machine_mode = value
        elif isinstance(value, str):
            self._machine_mode = MachineMode(value)
        else:
            raise TypeError(f"{__name__}.machine_mode must be of type MachineMode."
                            f" Got {type(value)}: {value}")

    @property
    def macro_restarted(self) -> bool:
        """Indicates if the current macro file was restarted after a pause"""
        return self._macro_restarted

    @macro_restarted.setter
    def macro_restarted(self, value: bool):
        self._macro_restarted = bool(value)

    @property
    def ms_up_time(self) -> int:
        """Millisecond fraction of `uptime`"""
        return self._ms_up_time

    @ms_up_time.setter
    def ms_up_time(self, value: int):
        self._ms_up_time = int(value)

    @property
    def next_tool(self) -> int:
        """Number of the next tool to be selected"""
        return self._next_tool

    @next_tool.setter
    def next_tool(self, value: int):
        self._next_tool = int(value)

    @property
    def plugins_started(self) -> bool:
        """Indicates if at least one plugin has been started"""
        return self._plugins_started

    @plugins_started.setter
    def plugins_started(self, value: bool):
        self._plugins_started = bool(value)

    @property
    def power_fail_script(self) -> str:
        """Script to execute when the power fails"""
        return self._power_fail_script

    @power_fail_script.setter
    def power_fail_script(self, value: str):
        self._power_fail_script = str(value)

    @property
    def previous_tool(self) -> int:
        """Number of the previous tool"""
        return self._previous_tool

    @previous_tool.setter
    def previous_tool(self, value: int):
        self._previous_tool = int(value)

    @property
    def restore_points(self) -> list[RestorePoint]:
        """List of restore points"""
        return self._restore_points

    @property
    def status(self) -> MachineStatus:
        """Current state of the machine"""
        return self._status

    @status.setter
    def status(self, value: MachineStatus):
        if isinstance(value, MachineStatus):
            self._status = value
        elif isinstance(value, str):
            self._status = MachineStatus(value)
        else:
            raise TypeError(f"{__name__}.status must be of type MachineStatus."
                            f" Got {type(value)}: {value}")

    @property
    def this_input(self) -> int | None:
        """Index of the current G-code input channel (see ObjectModel.Inputs)
        This is primarily intended for macro files to determine on which G-code channel it is running.
        The value of this property is always null in object model queries"""
        return self._this_input

    @this_input.setter
    def this_input(self, value: int | None = None):
        self._this_input = int(value) if value is not None else None

    @property
    def time(self) -> datetime | None:
        """Internal date and time in RepRapFirmware or null if unknown"""
        return self._time

    @time.setter
    def time(self, value: str | None = None):
        self._time = datetime.fromisoformat(value) if value is not None else None

    @property
    def up_time(self) -> int:
        """How long the machine has been running (in s)"""
        return self._up_time

    @up_time.setter
    def up_time(self, value: int):
        self._up_time = int(value)
