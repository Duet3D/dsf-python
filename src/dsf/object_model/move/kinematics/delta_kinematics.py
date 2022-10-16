from typing import List

from .delta_tower import DeltaTower
from ...model_object import ModelObject


class DeltaKinematics(ModelObject):
    """Delta kinematics"""
    def __init__(self):
        super().__init__()
        # Delta radius (in mm)
        self._delta_radius = 0
        # Homed height of a delta printer in mm
        self._homed_height = 0
        # Print radius for Hangprinter and Delta geometries (in mm)
        self._print_radius = 0
        # Delta tower properties
        self._towers = []
        # How much Z needs to be raised for each unit of movement in the +X direction
        self._x_tilt = 0
        # How much Z needs to be raised for each unit of movement in the +Y direction
        self._y_tilt = 0
        
    @property
    def delta_radius(self) -> float:
        """Delta radius (in mm)"""
        return self._delta_radius
    
    @delta_radius.setter
    def delta_radius(self, value):
        self._delta_radius = float(value) if value is not None else 0
    
    @property
    def homed_height(self) -> float:
        """Homed height of a delta printer in mm"""
        return self._homed_height
    
    @homed_height.setter
    def homed_height(self, value):
        self._homed_height = float(value) if value is not None else 0
    
    @property
    def print_radius(self) -> float:
        """Print radius for Hangprinter and Delta geometries (in mm)"""
        return self._print_radius
    
    @print_radius.setter
    def print_radius(self, value):
        self._print_radius = float(value) if value is not None else 0

    @property
    def towers(self) -> List[DeltaTower]:
        """Delta tower properties"""
        return self._towers
    
    @property
    def x_tilt(self) -> float:
        """How much Z needs to be raised for each unit of movement in the +X direction"""
        return self._x_tilt
    
    @x_tilt.setter
    def x_tilt(self, value):
        self._x_tilt = float(value) if value is not None else 0
    
    @property
    def y_tilt(self) -> float:
        """How much Z needs to be raised for each unit of movement in the +Y direction"""
        return self._y_tilt
    
    @y_tilt.setter
    def y_tilt(self, value):
        self._y_tilt = float(value) if value is not None else 0

    def _update_from_json(self, **kwargs) -> 'DeltaKinematics':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(DeltaKinematics, self)._update_from_json(**kwargs)
        self._towers = [DeltaTower.from_json(item) for item in kwargs.get('towers', [])]
        return self
