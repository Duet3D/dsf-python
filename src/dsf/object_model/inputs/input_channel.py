from .compatibility import Compatibility
from .distance_unit import DistanceUnit
from .input_channel_state import InputChannelState
from ..model_object import ModelObject
from ..utils import model_prop
from ...commands.code_channel import CodeChannel


class InputChannel(ModelObject):
    """Information about a G/M/T-code channel"""

    # True if the input is in active mode i.e. executing commands for its assigned motion system,
    # false if it is assigned to a motion system other than the current one
    active = model_prop("active", bool, False)

    # Whether relative positioning is being used
    axes_relative = model_prop("axes_relative", bool, False)

    # Emulation used on this channel
    compatibility = model_prop("compatibility", Compatibility, Compatibility.RepRapFirmware)

    # Whether inches are being used instead of mm
    distance_unit = model_prop("distance_unit", DistanceUnit, DistanceUnit.mm)

    # Whether relative extrusion is being used
    drives_relative = model_prop("drives_relative", bool, True)

    # Current feedrate in mm/s
    feed_rate = model_prop("feed_rate", float, 50.0)

    # Whether a macro file is being processed
    in_macro = model_prop("in_macro", bool, False)

    # Indicates if inverse time mode (G73) is active
    inverse_time_mode = model_prop("inverse_time_mode", bool, False)

    # Number of the current line
    line_number = model_prop("line_number", int, 0)

    # Indicates if the current macro file can be restarted after a pause
    macro_restartable = model_prop("macro_restartable", bool, False)

    # Active motion system index
    motion_system = model_prop("motion_system", int, 0)

    # Name of this channel
    name = model_prop("name", CodeChannel, CodeChannel.Unknown)

    # Index of the selected plane
    selected_plane = model_prop("selected_plane", int, 0)

    # Depth of the stack
    stack_depth = model_prop("stack_depth", int, 0)

    # State of this input channel
    state = model_prop("state", InputChannelState, InputChannelState.idle)

    # Whether volumetric extrusion is being used
    volumetric = model_prop("volumetric", bool, False)

    def __init__(self):
        super().__init__()
