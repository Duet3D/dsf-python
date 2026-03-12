from ..model_object import ModelObject


class ToolRetraction(ModelObject):
    """Tool retraction parameters"""

    def __init__(self) -> None:
        super().__init__()
        # Amount of additional filament to extrude when undoing a retraction (in mm)
        self._extra_restart: float = 0
        # Retraction length (in mm)
        self._length: float = 0
        # Retraction speed (in mm/s)
        self._speed: float = 0
        # Unretract speed (in mm/s)
        self._unretract_speed: float = 0
        # Amount of Z lift after doing a retraction (in mm)
        self._z_hop: float = 0
        
    @property
    def extra_restart(self) -> float:
        """Amount of additional filament to extrude when undoing a retraction (in mm)"""
        return self._extra_restart
    
    @extra_restart.setter
    def extra_restart(self, value: float | int | str):
        self._extra_restart = float(value)
        
    @property
    def length(self) -> float:
        """Retraction length (in mm)"""
        return self._length
    
    @length.setter
    def length(self, value: float | int | str):
        self._length = float(value)
        
    @property
    def speed(self) -> float:
        """Retraction speed (in mm/s)"""
        return self._speed
    
    @speed.setter
    def speed(self, value: float | int | str):
        self._speed = float(value)
        
    @property
    def unretract_speed(self) -> float:
        """Unretract speed (in mm/s)"""
        return self._unretract_speed
    
    @unretract_speed.setter
    def unretract_speed(self, value: float | int | str):
        self._unretract_speed = float(value)
        
    @property
    def z_hop(self) -> float:
        """Amount of Z lift after doing a retraction (in mm)"""
        return self._z_hop
    
    @z_hop.setter
    def z_hop(self, value: float | int | str):
        self._z_hop = float(value)
