from typing import List, Union

from ..model_object import ModelObject


class RestorePoint(ModelObject):
    """
    Class holding information about a restore point
    """
    def __init__(self):
        super(RestorePoint, self).__init__()

        # Axis coordinates of the restore point (in mm)
        self._coords = []
        # The virtual extruder position at the start of this move
        self._extruder_pos = 0
        # PWM value of the tool fan (0..1)
        self._fan_pwm = 0
        # Requested feedrate (in mm/s)
        self._feed_rate = 0
        # The output port bits setting for this move or null if not applicable
        self._io_bits = None
        # Laser PWM value (0..1) or null if not applicable
        self._laser_pwm = None
        # The spindle RPMs that were set, negative if anticlockwise direction
        self._spindle_speeds = []
        # The tool number that was active
        self._tool_number = -1
        
    @property
    def coords(self) -> List[float]:
        """Axis coordinates of the restore point (in mm)"""
        return self._coords
    
    @property
    def extruder_pos(self) -> float:
        """The virtual extruder position at the start of this move"""
        return self._extruder_pos
    
    @extruder_pos.setter
    def extruder_pos(self, value):
        self._extruder_pos = float(value) if value is not None else 0
        
    @property
    def fan_pwm(self) -> float:
        """PWM value of the tool fan (0..1)"""
        return self._fan_pwm
    
    @fan_pwm.setter
    def fan_pwm(self, value):
        self._fan_pwm = float(value) if value is not None else 0
        
    @property
    def feed_rate(self) -> float:
        """Requested feedrate (in mm/s)"""
        return self._feed_rate
    
    @feed_rate.setter
    def feed_rate(self, value):
        self._feed_rate = float(value) if value is not None else 0
        
    @property
    def io_bits(self) -> Union[int, None]:
        """The output port bits setting for this move or null if not applicable"""
        return self._io_bits
    
    @io_bits.setter
    def io_bits(self, value):
        self._io_bits = int(value) if value is not None else None
        
    @property
    def laser_pwm(self) -> Union[float, None]:
        """Laser PWM value (0..1) or null if not applicable"""
        return self._laser_pwm
    
    @laser_pwm.setter
    def laser_pwm(self, value):
        self._laser_pwm = float(value) if value is not None else None
        
    @property
    def spindle_speeds(self) -> List[float]:
        """The spindle RPMs that were set, negative if anticlockwise direction"""
        return self._spindle_speeds
    
    @property
    def tool_number(self) -> int:
        """The tool number that was active"""
        return self._tool_number
    
    @tool_number.setter
    def tool_number(self, value):
        self._tool_number = int(value) if value is not None else -1

    def _update_from_json(self, **kwargs) -> 'RestorePoint':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(RestorePoint, self)._update_from_json(**kwargs)
        self._coords = [float(c) for c in kwargs.get('coords', [])]
        self._spindle_speeds = [float(speed) for speed in kwargs.get('spindleSpeeds', [])]
        return self
