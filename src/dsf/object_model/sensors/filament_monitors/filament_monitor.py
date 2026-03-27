from .filament_monitor_enable_type import FilamentMonitorEnableMode
from .filament_monitor_status import FilamentMonitorStatus
from .filament_monitor_type import FilamentMonitorType
from ...model_object import ModelObject
from ...utils import model_prop


class FilamentMonitor(ModelObject):
    """Information about a filament monitor"""

    # Enable mode of this filament monitor
    enable_mode = model_prop("enable_mode", FilamentMonitorEnableMode, FilamentMonitorEnableMode.Disabled)

    # Last reported status of this filament monitor
    status = model_prop("status", FilamentMonitorStatus, FilamentMonitorStatus.NoDataReceived)

    # Type of this filament monitor
    type = model_prop("type", FilamentMonitorType, FilamentMonitorType.Unknown)

    def __init__(self, type_: FilamentMonitorType = FilamentMonitorType.Unknown):
        super(FilamentMonitor, self).__init__()
        self.type = type_

    @staticmethod
    def get_filament_monitor(type_: FilamentMonitorType):
        from .laser_filament_monitor import LaserFilamentMonitor
        from .pulsed_filament_monitor import PulsedFilamentMonitor
        from .rotating_magnet_filament_monitor import RotatingMagnetFilamentMonitor

        if isinstance(type_, str):
            type_ = FilamentMonitorType(type_)
        elif not isinstance(type_, FilamentMonitorType):
            raise TypeError(f"type must be of type FilamentMonitorType. Got {type(type_)}: {type_}")

        if type_ == FilamentMonitorType.Laser:
            return LaserFilamentMonitor()
        elif type_ == FilamentMonitorType.Pulsed:
            return PulsedFilamentMonitor()
        elif type_ == FilamentMonitorType.RotatingMagnet:
            return RotatingMagnetFilamentMonitor()
        else:
            return FilamentMonitor(type_)

    def _update_from_json(self, **kwargs):
        """Override ObjectModel._update_from_json to return the FilamentMonitorType type matching the given type"""
        if 'type_' in kwargs and self.type != FilamentMonitorType(kwargs.get('type_')):
            required_type = self.get_filament_monitor(kwargs.get('type_'))
            new_filament_monitor = required_type.update_from_json(kwargs)
            return new_filament_monitor

        super(FilamentMonitor, self)._update_from_json(**kwargs)
        return self
