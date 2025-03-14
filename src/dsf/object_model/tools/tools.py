from typing import List

from .tool_state import ToolState
from .tool_retraction import ToolRetraction
from ..model_object import ModelObject
from ...utils import deprecated


class Tool(ModelObject):
    """Information about a configured tool"""

    def __init__(self):
        super().__init__()
        # Active temperatures of the associated heaters (in C)
        self._active = []
        # Associated axes. At present only X and Y can be mapped per tool.
        self._axes = []
        # Extruder drives of this tool
        self._extruders = []
        # List of associated fans (indices)
        self._fans = []
        # Feedforward coefficients to apply to the mapped heaters during extrusions
        self._feed_forward = []
        self._feed_forward_pwm = []
        self._feed_forward_advance = None
        self._feed_forward_temp = []
        # Extruder drive index for resolving the tool filament (index or -1)
        self._filament_extruder = -1
        # List of associated heaters (indices)
        self._heaters = []
        # True if the filament has been firmware-retracted
        self._is_retracted = False
        # Mix ratios of the associated extruder drives
        self._mix = []
        # Name of this tool
        self._name = ""
        # Number of this tool
        self._number = 0
        # Axis offsets (in mm)
        self._offsets = []
        # Bitmap of the probed axis offsets
        self._offsets_probed = 0
        # Firmware retraction parameters
        self._retraction = ToolRetraction()
        # Index of the mapped spindle or -1 if not mapped
        self._spindle = 0
        # RPM of the mapped spindle
        self._spindle_rpm = 0
        # Standby temperatures of the associated heaters (in C)
        self._standby = []
        # Current state of this tool
        self._state = ToolState.off
        
    @property
    def active(self) -> List[float]:
        """Active temperatures of the associated heaters (in C)"""
        return self._active

    @property
    def axes(self) -> List[int]:
        """Associated axes. At present only X and Y can be mapped per tool.
        The order is the same as the visual axes, so by default the layout is
        [
            [0],    // X
            [1]     // Y
        ]
        Make sure to set each item individually so the change events are called"""
        return self._axes

    @property
    def extruders(self) -> List[int]:
        """Extruder drives of this tool"""
        return self._extruders

    @property
    def fans(self) -> List[int]:
        """List of associated fans (indices)"""
        return self._fans
    
    @property
    @deprecated("Use feed_forward_pwm instead.")
    def feed_forward(self) -> List[float]:
        """Feedforward coefficients to apply to the mapped heaters during extrusions"""
        return self._feed_forward
    
    @property
    def feed_forward_advance(self) -> float:
        """Time advance for applying feedforward in milliseconds"""
        return self._feed_forward_advance

    @feed_forward_advance.setter
    def feed_forward_advance(self, value):
        self._feed_forward_advance = float(value)

    @property
    def feed_forward_pwm(self) -> List[float]:
        """Feedforward coefficients to apply to the mapped heaters during extrusions"""
        return self._feed_forward_pwm

    @property
    def feed_forward_temp(self) -> List[float]:
        """Temperature increase per mm/dec extrusion speed"""
        return self._feed_forward_temp

    @property
    def filament_extruder(self) -> int:
        """Extruder drive index for resolving the tool filament (index or -1)"""
        return self._filament_extruder
    
    @filament_extruder.setter
    def filament_extruder(self, value):
        self._filament_extruder = int(value)
        
    @property
    def heaters(self) -> List[int]:
        """List of associated heaters (indices)"""
        return self._heaters
    
    @property
    def is_retracted(self) -> bool:
        """True if the filament has been firmware-retracted"""
        return self._is_retracted
    
    @is_retracted.setter
    def is_retracted(self, value):
        self._is_retracted = bool(value)
        
    @property
    def mix(self) -> List[float]:
        """Mix ratios of the associated extruder drives"""
        return self._mix
    
    @property
    def name(self) -> str:
        """Name of this tool"""
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = str(value)
        
    @property
    def number(self) -> int:
        """Number of this tool"""
        return self._number
    
    @number.setter
    def number(self, value):
        self._number = int(value)
        
    @property
    def offsets(self) -> List[float]:
        """Axis offsets (in mm)
        This list is in the same order as Move.Axes"""
        return self._offsets
    
    @property
    def offsets_probed(self) -> int:
        """Bitmap of the probed axis offsets"""
        return self._offsets_probed
    
    @offsets_probed.setter
    def offsets_probed(self, value):
        self._offsets_probed = int(value)
        
    @property
    def retraction(self) -> ToolRetraction:
        """Firmware retraction parameters"""
        return self._retraction
    
    @property
    def spindle(self) -> int:
        """Index of the mapped spindle or -1 if not mapped"""
        return self._spindle
    
    @spindle.setter
    def spindle(self, value):
        self._spindle = int(value)
        
    @property
    def spindle_rpm(self) -> int:
        """RPM of the mapped spindle"""
        return self._spindle_rpm
    
    @spindle_rpm.setter
    def spindle_rpm(self, value):
        self._spindle_rpm = int(value)
        
    @property
    def standby(self) -> List[float]:
        """Standby temperatures of the associated heaters (in C)"""
        return self._standby
    
    @property
    def state(self) -> ToolState:
        """Current state of this tool"""
        return self._state
    
    @state.setter
    def state(self, value):
        if value is None or value == "":
            self._state = ToolState.off
        elif isinstance(value, ToolState):
            self._state = value
        elif isinstance(value, str):
            self._state = ToolState(value)
        else:
            raise TypeError(f"{__name__}.state must be of type ToolState. Got {type(value)}: {value}")
