from .Duet3DFilamentMonitor import Duet3DFilamentMonitor
from .filament_monitor_type import FilamentMonitorType
from ...model_object import ModelObject
from ...utils import model_prop, nullable_model_prop


class LaserFilamentMonitorCalibrated(ModelObject):
    """Calibrated properties of a laser filament monitor"""

    # Maximum percentage (0..1 or greater)
    percent_max = model_prop("percent_max", float, 0)

    # Minimum percentage (0..1)
    percent_min = model_prop("percent_min", float, 0)

    # Calibrated sensitivity
    sensitivity = model_prop("sensitivity", float, 0)

    # Total extruded distance (in mm)
    total_distance = model_prop("total_distance", float, 0)

    def __init__(self):
        super(LaserFilamentMonitorCalibrated, self).__init__()


class LaserFilamentMonitorConfigured(ModelObject):
    """Configured  properties of a laser filament monitor"""

    # Whether all moves and not only printing moves are supposed to be checked
    all_moves = model_prop("all_moves", bool, False)

    # Calibration factor of this sensor
    calibration_factor = model_prop("calibration_factor", float, 0)

    # Maximum percentage (0..1 or greater)
    percent_max = model_prop("percent_max", float, 0)

    # Minimum percentage (0..1)
    percent_min = model_prop("percent_min", float, 0)

    # Sample distance (in mm)
    sample_distance = model_prop("sample_distance", float, 0)

    def __init__(self):
        super(LaserFilamentMonitorConfigured, self).__init__()


class LaserFilamentMonitor(Duet3DFilamentMonitor):
    """Information about a laser filament monitor"""

    # Calibrated properties of this filament monitor
    calibrated = nullable_model_prop('calibrated', LaserFilamentMonitorCalibrated)

    # Configured properties of this filament monitor
    configured = model_prop('configured', LaserFilamentMonitorConfigured, LaserFilamentMonitorConfigured())

    def __init__(self):
        super(LaserFilamentMonitor, self).__init__(FilamentMonitorType.Laser)
