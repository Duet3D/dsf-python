from typing import Union

from .Duet3DFilamentMonitor import Duet3DFilamentMonitor
from .filament_monitor_type import FilamentMonitorType
from ...model_object import ModelObject
from ...utils import wrap_model_property


class LaserFilamentMonitorCalibrated(ModelObject):
    """Calibrated properties of a laser filament monitor"""

    def __init__(self):
        super(LaserFilamentMonitorCalibrated, self).__init__()
        self._calibration_factor = 0
        self._percent_max = 0
        self._percent_min = 0
        self._sensivity = 0
        self._total_distance = 0

    @property
    def calibration_factor(self) -> float:
        """Calibration factor of this sensor"""
        return self._calibration_factor

    @calibration_factor.setter
    def calibration_factor(self, value):
        self._calibration_factor = float(value)

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
    def sensivity(self) -> float:
        """Calibrated sensivity"""
        return self._sensivity

    @sensivity.setter
    def sensivity(self, value):
        self._sensivity = float(value)

    @property
    def total_distance(self) -> float:
        """Total extruded distance (in mm)"""
        return self._total_distance

    @total_distance.setter
    def total_distance(self, value):
        self._total_distance = float(value)


class LaserFilamentMonitorConfigured(ModelObject):
    """Configured  properties of a laser filament monitor"""

    def __init__(self):
        super(LaserFilamentMonitorConfigured, self).__init__()
        self._all_moves = False
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


class LaserFilamentMonitor(Duet3DFilamentMonitor):
    """Information about a laser filament monitor"""

    # Calibrated properties of this filament monitor
    calibrated = wrap_model_property('calibrated', LaserFilamentMonitorCalibrated)

    def __init__(self):
        super(LaserFilamentMonitor, self).__init__()
        self._calibrated = None
        self._configured = LaserFilamentMonitorConfigured()
        self._filament_present = False
        self._type = FilamentMonitorType.Laser

    @property
    def configured(self) -> LaserFilamentMonitorConfigured:
        """Configured properties of this filament monitor"""
        return self._configured

    @property
    def filament_present(self) -> Union[bool, None]:
        """Indicates if a filament is present"""
        return self._filament_present

    @filament_present.setter
    def filament_present(self, value):
        self._filament_present = bool(value) if value is not None else None
