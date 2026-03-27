from .filament_monitor import FilamentMonitor
from .filament_monitor_type import FilamentMonitorType
from ...utils import model_prop, nullable_model_prop


class Duet3DFilamentMonitor(FilamentMonitor):
    """Base class for Duet3D filament monitors"""

    # Average ratio of measured vs. commanded movement
    avg_percentage = nullable_model_prop("avg_percentage", int)

    # Last ratio of measured vs. commanded movement
    last_percentage = nullable_model_prop("last_percentage", int)

    # Maximum ratio of measured vs. commanded movement
    max_percentage = nullable_model_prop("max_percentage", int)

    # Minimum ratio of measured vs. commanded movement
    min_percentage = nullable_model_prop("min_percentage", int)

    # Position of the sensor (in mm)
    position = model_prop("position", float, 0)

    # Total extrusion commanded (in mm)
    total_extrusion = model_prop("total_extrusion", float, 0)

    def __init__(self, type_: FilamentMonitorType = FilamentMonitorType.Unknown):
        super(Duet3DFilamentMonitor, self).__init__(type_)
