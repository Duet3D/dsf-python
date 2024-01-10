from .compatibility import Compatibility
from .distance_unit import DistanceUnit
from .input_channel_state import InputChannelState
from ..model_object import ModelObject
from ...commands.code_channel import CodeChannel


class InputChannel(ModelObject):
    """Information about a G/M/T-code channel"""
    
    def __init__(self):
        super().__init__()
        # True if the input is in active mode i.e. executing commands for its assigned motion system,
        # false if it is assigned to a motion system other than the current one
        # This will always be true except for the File and File2 inputs
        self._active = False
        # Whether relative positioning is being used
        self._axes_relative = False
        # Emulation used on this channel
        self._compatibility = Compatibility.RepRapFirmware
        # Whether inches are being used instead of mm
        self._distance_unit = DistanceUnit.mm
        # Whether relative extrusion is being used
        self._drives_relative = True
        # Current feedrate in mm/s
        self._feed_rate = 50.0
        # Whether a macro file is being processed
        self._in_macro = False
        # Indicates if inverse time mode (G73) is active
        self._inverse_time_mode = False
        # Indicates if the current macro file can be restarted after a pause
        self._macro_restartable = False
        # Active motion system index
        self._motion_system = 0
        # Name of this channel
        self._name = CodeChannel.Unknown
        # Index of the selected plane
        self._selected_plane = 0
        # Depth of the stack
        self._stack_depth = 0
        # State of this input channel
        self._state = InputChannelState.idle
        # Number of the current line
        self._line_number = 0
        # Whether volumetric extrusion is being used
        self._volumetric = False

    @property
    def active(self) -> bool:
        """True if the input is in active mode i.e. executing commands for its assigned motion system,
        False if it is assigned to a motion system other than the current one.
        This will always be true except for the File and File2 inputs"""
        return self._active

    @active.setter
    def active(self, value):
        self._active = bool(value)

    @property
    def axes_relative(self) -> bool:
        """Whether relative positioning is being used"""
        return self._axes_relative

    @axes_relative.setter
    def axes_relative(self, value: bool):
        self._axes_relative = bool(value)

    @property
    def compatibility(self) -> Compatibility:
        """Emulation used on this channel"""
        return self._compatibility

    @compatibility.setter
    def compatibility(self, value: Compatibility):
        if isinstance(value, Compatibility):
            self._compatibility = value
        elif isinstance(value, str):
            self._compatibility = Compatibility(value)
        else:
            raise TypeError(f"{__name__}.compatibility must be of type Compatibility."
                            f" Got {type(value)}: {value}")

    @property
    def distance_unit(self) -> DistanceUnit:
        """Whether inches are being used instead of mm"""
        return self._distance_unit

    @distance_unit.setter
    def distance_unit(self, value: DistanceUnit):
        if isinstance(value, DistanceUnit):
            self._distance_unit = value
        elif isinstance(value, str):
            self._distance_unit = DistanceUnit(value)
        else:
            raise TypeError(f"{__name__}.distance_unit must be of type DistanceUnit."
                            f" Got {type(value)}: {value}")

    @property
    def drives_relative(self) -> bool:
        """Whether relative extrusion is being used"""
        return self._drives_relative

    @drives_relative.setter
    def drives_relative(self, value: bool):
        self._drives_relative = bool(value)

    @property
    def feed_rate(self) -> float:
        """Current feedrate in mm/s"""
        return self._feed_rate

    @feed_rate.setter
    def feed_rate(self, value):
        self._feed_rate = float(value)

    @property
    def in_macro(self) -> bool:
        """Whether a macro file is being processed"""
        return self._in_macro

    @in_macro.setter
    def in_macro(self, value: bool):
        self._in_macro = bool(value)

    @property
    def inverse_time_mode(self) -> bool:
        """Indicates if inverse time mode (G73) is active"""
        return self._inverse_time_mode

    @inverse_time_mode.setter
    def inverse_time_mode(self, value):
        self._inverse_time_mode = bool(value)

    @property
    def line_number(self) -> int:
        """Number of the current line"""
        return self._line_number

    @line_number.setter
    def line_number(self, value):
        self._line_number = int(value)

    @property
    def macro_restartable(self) -> bool:
        """Indicates if the current macro file can be restarted after a pause"""
        return self._macro_restartable

    @macro_restartable.setter
    def macro_restartable(self, value: bool):
        self._macro_restartable = bool(value)

    @property
    def motion_system(self) -> int:
        """Active motion system index"""
        return self._motion_system

    @motion_system.setter
    def motion_system(self, value):
        self._motion_system = int(value)

    @property
    def name(self) -> CodeChannel:
        """Name of this channel"""
        return self._name

    @name.setter
    def name(self, value: CodeChannel):
        if isinstance(value, CodeChannel):
            self._name = value
        elif isinstance(value, str):
            self._name = CodeChannel(value)
        else:
            raise TypeError(f"{__name__}.name must be of type CodeChannel. "
                            f"Got {type(value)}: {value}")

    @property
    def selected_plane(self) -> int:
        """Index of the selected plane"""
        return self._selected_plane

    @selected_plane.setter
    def selected_plane(self, value):
        self._selected_plane = int(value)

    @property
    def stack_depth(self) -> int:
        """Depth of the stack"""
        return self._stack_depth

    @stack_depth.setter
    def stack_depth(self, value):
        self._stack_depth = int(value)

    @property
    def state(self) -> InputChannelState:
        """State of this input channel"""
        return self._state

    @state.setter
    def state(self, value: InputChannelState):
        if isinstance(value, InputChannelState):
            self._state = value
        elif isinstance(value, str):
            self._state = InputChannelState(value)
        else:
            raise TypeError(f"{__name__}.state must be of type InputChannelState. "
                            f"Got {type(value)}: {value}")

    @property
    def volumetric(self) -> bool:
        """Whether volumetric extrusion is being used"""
        return self._volumetric

    @volumetric.setter
    def volumetric(self, value: bool):
        self._volumetric = bool(value)
