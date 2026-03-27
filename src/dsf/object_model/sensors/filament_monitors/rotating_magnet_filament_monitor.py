from .Duet3DFilamentMonitor import Duet3DFilamentMonitor
from .filament_monitor_type import FilamentMonitorType
from ...model_object import ModelObject
from ...utils import model_prop, nullable_model_prop


class RotatingMagnetFilamentMonitorCalibrated(ModelObject):
    """Calibrated properties of a rotating magnet filament monitor"""

    # Extruded distance per pulse (in mm)
    mm_per_pulse = model_prop("mm_per_pulse", float, 0)

    # Maximum percentage (0..1 or greater)
    percent_max = model_prop("percent_max", float, 0)

    # Minimum percentage (0..1)
    percent_min = model_prop("percent_min", float, 0)

    # Total extruded distance (in mm)
    total_distance = model_prop("total_distance", float, 0)

    def __init__(self):
        super(RotatingMagnetFilamentMonitorCalibrated, self).__init__()


class RotatingMagnetFilamentMonitorConfigured(ModelObject):
    """Configured properties of a rotating magnet filament monitor"""

    # Whether all moves and not only printing moves are supposed to be checked
    all_moves = model_prop("all_moves", bool, False)

    # Extruded distance per revolution (in mm)
    mm_per_rev = model_prop("mm_per_rev", float, 0)

    # Maximum percentage (0..1 or greater)
    percent_max = model_prop("percent_max", float, 0)

    # Minimum percentage (0..1)
    percent_min = model_prop("percent_min", float, 0)

    # Sample distance (in mm)
    sample_distance = model_prop("sample_distance", float, 0)

    def __init__(self):
        super(RotatingMagnetFilamentMonitorConfigured, self).__init__()


class RotatingMagnetFilamentMonitor(Duet3DFilamentMonitor):
    """Information about a rotating magnet filament monitor"""

    # Calibrated properties of this filament monitor
    calibrated = nullable_model_prop('calibrated', RotatingMagnetFilamentMonitorCalibrated)

    # Configured properties of this filament monitor
    configured = model_prop('configured', RotatingMagnetFilamentMonitorConfigured)

    def __init__(self):
        super(RotatingMagnetFilamentMonitor, self).__init__(FilamentMonitorType.RotatingMagnet)
