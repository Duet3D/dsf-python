from .filament_monitor_enable_type import FilamentMonitorEnableMode
from .filament_monitor_status import FilamentMonitorStatus
from .filament_monitor_type import FilamentMonitorType
from ...model_object import ModelObject
from ...utils import model_prop, nullable_model_prop
from ....utils import JSONElement


class FilamentMonitor(ModelObject):
    """Information about a filament monitor"""

    # Whether this filament monitor is enabled
    # Obsolete: use enable_mode instead
    enabled = model_prop("enabled", bool, False)

    # Enable mode of this filament monitor
    enable_mode = model_prop("enable_mode", FilamentMonitorEnableMode, FilamentMonitorEnableMode.Disabled)

    # Indicates if filament is present in this filament monitor (None if unknown)
    filament_present = nullable_model_prop("filament_present", bool)

    # Last reported status of this filament monitor
    status = model_prop("status", FilamentMonitorStatus, FilamentMonitorStatus.NoDataReceived)

    # Type of this filament monitor
    type = model_prop("type", FilamentMonitorType, FilamentMonitorType.Unknown)

    def __init__(self, type_: FilamentMonitorType = FilamentMonitorType.Unknown):
        super(FilamentMonitor, self).__init__()
        self.type = type_

    @staticmethod
    def get_filament_monitor(type_: FilamentMonitorType | str) -> "FilamentMonitor":
        from .laser_filament_monitor import LaserFilamentMonitor
        from .pulsed_filament_monitor import PulsedFilamentMonitor
        from .rotating_magnet_filament_monitor import RotatingMagnetFilamentMonitor

        type_ = FilamentMonitorType(type_)

        if type_ == FilamentMonitorType.Laser:
            return LaserFilamentMonitor()
        elif type_ == FilamentMonitorType.Pulsed:
            return PulsedFilamentMonitor()
        elif type_ == FilamentMonitorType.RotatingMagnet:
            return RotatingMagnetFilamentMonitor()
        else:
            return FilamentMonitor(type_)

    def _update_from_json(self, **kwargs: JSONElement) -> "FilamentMonitor":
        """Override ObjectModel._update_from_json to return the FilamentMonitorType type matching the given type"""
        type_ = kwargs.get('type_')
        if isinstance(type_, str) and self.type != FilamentMonitorType(type_):
            return self.get_filament_monitor(type_).update_from_json(kwargs)

        super(FilamentMonitor, self)._update_from_json(**kwargs)
        return self
