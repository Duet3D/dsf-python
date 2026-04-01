from datetime import datetime
from typing import Optional

from .beep_request import BeepRequest
from .gp_output_port import GpOutputPort
from .log_level import LogLevel
from .machine_mode import MachineMode
from .machine_status import MachineStatus
from .message_box import MessageBox
from .restore_point import RestorePoint
from .startup_error import StartupError
from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import model_prop, nullable_model_prop


class State(ModelObject):
    """Information about the machine state"""

    atx_power = nullable_model_prop('atx_power', bool)
    atx_power_port = nullable_model_prop('atx_power_port', str)
    beep = nullable_model_prop('beep', BeepRequest)
    current_tool = model_prop('current_tool', int, -1)
    deferred_power_down = nullable_model_prop('deferred_power_down', bool)
    display_message = model_prop('display_message', str, "")
    gp_out = model_prop('gp_out', ModelCollection[Optional[GpOutputPort]], ModelCollection(Optional[GpOutputPort]))
    laser_pwm = nullable_model_prop('laser_pwm', float)
    log_file = nullable_model_prop('log_file', str)
    log_level = model_prop('log_level', LogLevel, LogLevel.Off)
    message_box = nullable_model_prop('message_box', MessageBox)
    machine_mode = model_prop('machine_mode', MachineMode, MachineMode.FFF)
    macro_restarted = model_prop('macro_restarted', bool, False)
    ms_up_time = model_prop('ms_up_time', int)
    next_tool = model_prop('next_tool', int, -1)
    plugins_started = model_prop('plugins_started', bool, False)
    power_fail_script = model_prop('power_fail_script', str, "")
    previous_tool = model_prop('previous_tool', int, -1)
    restore_points = model_prop('restore_points', ModelCollection[RestorePoint], ModelCollection(RestorePoint))
    startup_error = nullable_model_prop('startup_error', StartupError)
    status = model_prop('status', MachineStatus, MachineStatus.starting)
    this_active = nullable_model_prop('this_active', bool)
    this_input = nullable_model_prop('this_input', int)
    time = nullable_model_prop('time', datetime, lambda: None)
    up_time = model_prop('up_time', int, 0)

    def __init__(self):
        super(State, self).__init__()
