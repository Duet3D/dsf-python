from .filament_monitor_base import FilamentMonitorBase
from .filament_monitor_type import FilamentMonitorType
from .laser_filament_monitor import LaserFilamentMonitor
from .pulsed_filament_monitor import PulsedFilamentMonitor
from .rotating_magnet_filament_monitor import RotatingMagnetFilamentMonitor


def get_filament_monitor(type_: FilamentMonitorType) -> FilamentMonitorBase:
    if type_ == FilamentMonitorType.Laser:
        return LaserFilamentMonitor()
    elif type_ == FilamentMonitorType.Pulsed:
        return PulsedFilamentMonitor()
    elif type_ == FilamentMonitorType.RotatingMagnet:
        return RotatingMagnetFilamentMonitor()
    else:
        return FilamentMonitorBase(type_)
