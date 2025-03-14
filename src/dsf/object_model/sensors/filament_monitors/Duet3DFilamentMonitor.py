
from typing import Union

from .filament_monitor import FilamentMonitor
from .filament_monitor_type import FilamentMonitorType


class Duet3DFilamentMonitor(FilamentMonitor):
    """Base class for Duet3D filament monitors"""
    def __init__(self, type_: FilamentMonitorType = FilamentMonitorType.Unknown):
        super(Duet3DFilamentMonitor, self).__init__(type_)
        # Average ratio of measured vs. commanded movement
        self._avg_percentage = None
        # Last ratio of measured vs. commanded movement
        self._last_percentage = None
        # Maximum ratio of measured vs. commanded movement
        self._max_percentage = None
        # Minimum ratio of measured vs. commanded movement
        self._min_percentage = None
        # Position of the sensor (in mm)
        self._position = 0
        # Total extrusion commanded (in mm)
        self._total_extrusion = 0
        
    @property
    def avg_percentage(self) -> Union[int, None]:
        """Average ratio of measured vs. commanded movement"""
        return self._avg_percentage
    
    @avg_percentage.setter
    def avg_percentage(self, value):
        self._avg_percentage = None if value is None else int(value)

    @property
    def last_percentage(self) -> Union[int, None]:
        """Last ratio of measured vs. commanded movement"""
        return self._last_percentage
    
    @last_percentage.setter
    def last_percentage(self, value):
        self._last_percentage = None if value is None else int(value)

    @property
    def max_percentage(self) -> Union[int, None]:
        """Maximum ratio of measured vs. commanded movement"""
        return self._max_percentage
    
    @max_percentage.setter
    def max_percentage(self, value):
        self._max_percentage = None if value is None else int(value)

    @property
    def min_percentage(self) -> Union[int, None]:
        """Minimum ratio of measured vs. commanded movement"""
        return self._min_percentage
    
    @min_percentage.setter
    def min_percentage(self, value):
        self._min_percentage = None if value is None else int(value)

    @property
    def position(self) -> float:
        """Position of the sensor (in mm)"""
        return self._position

    @position.setter
    def position(self, value):
        self._position = float(value)
    
    @property
    def total_extrusion(self) -> float:
        """Total extrusion commanded (in mm)"""
        return self._total_extrusion
    
    @total_extrusion.setter
    def total_extrusion(self, value):
        self._total_extrusion = float(value)
