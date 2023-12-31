from .Duet3DFilamentMonitor import Duet3DFilamentMonitor
from .filament_monitor_type import FilamentMonitorType
from ...model_object import ModelObject
from ...utils import wrap_model_property


class RotatingMagnetFilamentMonitorCalibrated(ModelObject):
    """Calibrated properties of a rotating magnet filament monitor"""

    def __init__(self):
        super(RotatingMagnetFilamentMonitorCalibrated, self).__init__()
        self._mm_per_pulse = 0
        self._percent_max = 0
        self._percent_min = 0
        self._total_distance = 0

    @property
    def mm_per_pulse(self) -> float:
        """Extruded distance per pulse (in mm)"""
        return self._mm_per_pulse

    @mm_per_pulse.setter
    def mm_per_pulse(self, value):
        self._mm_per_pulse = float(value)

    @property
    def percent_max(self) -> float:
        """Maximum percentage (0..1 or greater)"""
        return self._percent_max

    @percent_max.setter
    def percent_max(self, value):
        self._percent_max = float(value)

    @property
    def percent_min(self) -> float:
        """Minimum percentage (0..1)"""
        return self._percent_min

    @percent_min.setter
    def percent_min(self, value):
        self._percent_min = float(value)

    @property
    def total_distance(self) -> float:
        """Total extruded distance (in mm)"""
        return self._total_distance

    @total_distance.setter
    def total_distance(self, value):
        self._total_distance = float(value)


class RotatingMagnetFilamentMonitorConfigured(ModelObject):
    """Configured properties of a rotating magnet filament monitor"""

    def __init__(self):
        super(RotatingMagnetFilamentMonitorConfigured, self).__init__()
        self._all_moves = False
        self._mm_per_rev = 0
        self._percent_max = 0
        self._percent_min = 0
        self._sample_distance = 0

    @property
    def all_moves(self) -> bool:
        """Whether all moves and not only printing moves are supposed to be checked"""
        return self._all_moves
    
    @all_moves.setter
    def all_moves(self, value):
        self._all_moves = bool(value)
        
    @property
    def mm_per_rev(self) -> float:
        """Extruded distance per revolution (in mm)"""
        return self._mm_per_rev
    
    @mm_per_rev.setter
    def mm_per_rev(self, value):
        self._mm_per_rev = float(value)
        
    @property
    def percent_max(self) -> float:
        """Maximum percentage (0..1 or greater)"""
        return self._percent_max
    
    @percent_max.setter
    def percent_max(self, value):
        self._percent_max = float(value)
        
    @property
    def percent_min(self) -> float:
        """Minimum percentage (0..1)"""
        return self._percent_min
    
    @percent_min.setter
    def percent_min(self, value):
        self._percent_min = float(value)
        
    @property
    def sample_distance(self) -> float:
        """Sample distance (in mm)"""
        return self._sample_distance
    
    @sample_distance.setter
    def sample_distance(self, value):
        self._sample_distance = float(value)


class RotatingMagnetFilamentMonitor(Duet3DFilamentMonitor):
    """Information about a rotating magnet filament monitor"""

    # Calibrated properties of this filament monitor
    calibrated = wrap_model_property('calibrated', RotatingMagnetFilamentMonitorCalibrated)

    def __init__(self):
        super(RotatingMagnetFilamentMonitor, self).__init__()
        self._calibrated = None
        self._configured = RotatingMagnetFilamentMonitorConfigured()
        self._type = FilamentMonitorType.RotatingMagnet

    @property
    def configured(self) -> RotatingMagnetFilamentMonitorConfigured:
        """Configured properties of this filament monitor"""
        return self._configured
