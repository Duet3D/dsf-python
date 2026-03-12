from typing import SupportsFloat

from ...model_object import ModelObject


class DeltaTower(ModelObject):
    """Delta tower properties"""

    def __init__(self) -> None:
        super().__init__()
        # Tower position corrections (in degrees)
        self._angle_correction: float = 0
        # Diagonal rod length (in mm)
        self._diagonal: float = 0
        # Deviation of the ideal endstop position (in mm)
        self._endstop_adjustment: float = 0
        # X coordinate of this tower (in mm)
        self._x_pos: float = 0
        # Y coordinate of this tower (in mm)
        self._y_pos: float = 0
        
    @property
    def angle_correction(self) -> float:
        """Tower position corrections (in degrees)"""
        return self._angle_correction
    
    @angle_correction.setter
    def angle_correction(self, value: SupportsFloat | str) -> None:
        self._angle_correction = float(value)
        
    @property
    def diagonal(self) -> float:
        """Diagonal rod length (in mm)"""
        return self._diagonal
    
    @diagonal.setter
    def diagonal(self, value: SupportsFloat | str) -> None:
        self._diagonal = float(value)
        
    @property
    def endstop_adjustment(self) -> float:
        """Deviation of the ideal endstop position (in mm)"""
        return self._endstop_adjustment
    
    @endstop_adjustment.setter
    def endstop_adjustment(self, value: SupportsFloat | str) -> None:
        self._endstop_adjustment = float(value)
        
    @property
    def x_pos(self) -> float:
        """X coordinate of this tower (in mm)"""
        return self._x_pos
    
    @x_pos.setter
    def x_pos(self, value: SupportsFloat | str) -> None:
        self._x_pos = float(value)
        
    @property
    def y_pos(self) -> float:
        """Y coordinate of this tower (in mm)"""
        return self._y_pos
    
    @y_pos.setter
    def y_pos(self, value: SupportsFloat | str) -> None:
        self._y_pos = float(value)
