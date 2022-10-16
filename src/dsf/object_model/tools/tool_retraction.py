from ..model_object import ModelObject


class ToolRetraction(ModelObject):
    """Tool retraction parameters"""

    def __init__(self):
        super().__init__()
        # Amount of additional filament to extrude when undoing a retraction (in mm)
        self._extra_restart = 0
        # Retraction length (in mm)
        self._length = 0
        # Retraction speed (in mm/s)
        self._speed = 0
        # Unretract speed (in mm/s)
        self._unretract_speed = 0
        # Amount of Z lift after doing a retraction (in mm)
        self._zhop = 0
        
    @property
    def extra_restart(self) -> float:
        """Amount of additional filament to extrude when undoing a retraction (in mm)"""
        return self._extra_restart
    
    @extra_restart.setter
    def extra_restart(self, value):
        self._extra_restart = float(value) if value is not None else 0
        
    @property
    def length(self) -> float:
        """Retraction length (in mm)"""
        return self._length
    
    @length.setter
    def length(self, value):
        self._length = float(value) if value is not None else 0
        
    @property
    def speed(self) -> float:
        """Retraction speed (in mm/s)"""
        return self._speed
    
    @speed.setter
    def speed(self, value):
        self._speed = float(value) if value is not None else 0
        
    @property
    def unretract_speed(self) -> float:
        """Unretract speed (in mm/s)"""
        return self._unretract_speed
    
    @unretract_speed.setter
    def unretract_speed(self, value):
        self._unretract_speed = float(value) if value is not None else 0
        
    @property
    def zhop(self) -> float:
        """Amount of Z lift after doing a retraction (in mm)"""
        return self._zhop
    
    @zhop.setter
    def zhop(self, value):
        self._zhop = float(value) if value is not None else 0
