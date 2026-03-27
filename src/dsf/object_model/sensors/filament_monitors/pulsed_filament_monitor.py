from .filament_monitor import FilamentMonitor
from .filament_monitor_type import FilamentMonitorType
from ...model_object import ModelObject
from ...utils import model_prop, nullable_model_prop


class PulsedFilamentMonitorCalibrated(ModelObject):
    """Calibrated properties of a pulsed filament monitor"""

    # Extruded distance per pulse (in mm)
    mm_per_pulse = model_prop("mm_per_pulse", float, 0)

    # Maximum percentage (0..1 or greater)
    percent_max = model_prop("percent_max", float, 0)

    # Minimum percentage (0..1)
    percent_min = model_prop("percent_min", float, 0)

    # Total extruded distance (in mm)
    total_distance = model_prop("total_distance", float, 0)

    def __init__(self):
        super(PulsedFilamentMonitorCalibrated, self).__init__()


class PulsedFilamentMonitorConfigured(ModelObject):
    """Configured properties of a pulsed filament monitor"""

    # Extruded distance per pulse (in mm)
    mm_per_pulse = model_prop("mm_per_pulse", float, 0)

    # Maximum percentage (0..1 or greater)
    percent_max = model_prop("percent_max", float, 0)

    # Minimum percentage (0..1)
    percent_min = model_prop("percent_min", float, 0)

    # Sample distance (in mm)
    sample_distance = model_prop("sample_distance", float, 0)

    def __init__(self):
        super(PulsedFilamentMonitorConfigured, self).__init__()


class PulsedFilamentMonitor(FilamentMonitor):
    """Information about a pulsed filament monitor"""

    # Calibrated properties of this filament monitor
    calibrated = nullable_model_prop('calibrated', PulsedFilamentMonitorCalibrated)

    # Configured properties of this filament monitor
    configured = model_prop('configured', PulsedFilamentMonitorConfigured, PulsedFilamentMonitorConfigured())

    # Position of the sensor (in mm)
    position = model_prop('position', float)

    def __init__(self):
        super(PulsedFilamentMonitor, self).__init__(FilamentMonitorType.Pulsed)
