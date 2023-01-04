from .filament_monitor_status import FilamentMonitorStatus
from .filament_monitor_type import FilamentMonitorType
from ...model_object import ModelObject


class FilamentMonitor(ModelObject):
    """Information about a filament monitor"""

    def __init__(self, type_: FilamentMonitorType = FilamentMonitorType.Unknown):
        super(FilamentMonitor, self).__init__()
        self._enabled = False
        self._status = FilamentMonitorStatus.NoDataReceived
        self._type = type_

    @property
    def enabled(self) -> bool:
        """Indicates if this filament monitor is enabled"""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = bool(value)

    @staticmethod
    def get_filament_monitor(type_: FilamentMonitorType) -> 'FilamentMonitor':
        from .laser_filament_monitor import LaserFilamentMonitor
        from .pulsed_filament_monitor import PulsedFilamentMonitor
        from .rotating_magnet_filament_monitor import RotatingMagnetFilamentMonitor

        if isinstance(type_, str):
            type_ = FilamentMonitorType(type_)
        elif not isinstance(type_, FilamentMonitorType):
            raise TypeError(f"type must be of type FilamentMonitorType."
                            f" Got {type(type_)}: {type_}")

        if type_ == FilamentMonitorType.Laser:
            return LaserFilamentMonitor()
        elif type_ == FilamentMonitorType.Pulsed:
            return PulsedFilamentMonitor()
        elif type_ == FilamentMonitorType.RotatingMagnet:
            return RotatingMagnetFilamentMonitor()
        else:
            return FilamentMonitor(type_)

    @property
    def status(self) -> FilamentMonitorStatus:
        """Last reported status of this filament monitor"""
        return self._status

    @status.setter
    def status(self, value: FilamentMonitorStatus = FilamentMonitorStatus.NoDataReceived):
        if isinstance(value, FilamentMonitorStatus):
            self._status = value
        elif isinstance(value, str):
            self._status = FilamentMonitorStatus(value)
        else:
            raise TypeError(f"{__name__}.status must be of type FilamentMonitorStatus."
                            f" Got {type(value)}: {value}")

    @property
    def type(self) -> FilamentMonitorType:
        """Type of this filament monitor"""
        return self._type

    def _update_from_json(self, **kwargs) -> 'FilamentMonitor':
        """Override ObjectModel._update_from_json to return the FilamentMonitorType type matching the given type"""
        if 'type_' in kwargs and self.type != FilamentMonitorType(kwargs.get('type_')):
            required_type = self.get_filament_monitor(kwargs.get('type_'))
            new_filament_monitor = required_type.update_from_json(kwargs)
            return new_filament_monitor

        super(FilamentMonitor, self)._update_from_json(**kwargs)
        return self
