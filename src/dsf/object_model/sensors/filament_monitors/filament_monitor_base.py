from .filament_monitor_status import FilamentMonitorStatus
from .filament_monitor_type import FilamentMonitorType
from ...model_object import ModelObject


class FilamentMonitorBase(ModelObject):

    def __init__(self, type_: FilamentMonitorType = FilamentMonitorType.Unknown):
        super(FilamentMonitorBase, self).__init__()
        self._enabled = False
        self._status = None
        self._type = type_

    @property
    def enabled(self) -> bool:
        """Indicates if this filament monitor is enabled"""
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = bool(value)

    @property
    def status(self) -> FilamentMonitorStatus:
        """Last reported status of this filament monitor"""
        return self._status

    @status.setter
    def status(self, value):
        if value is None:
            self._status = FilamentMonitorStatus.NoDataReceived
        elif isinstance(value, FilamentMonitorStatus):
            self._status = value
        elif isinstance(value, str):
            self._type = FilamentMonitorStatus(value)
        else:
            raise TypeError(f"{__name__}.status must be of type FilamentMonitorStatus. Got {type(value)}: {value}")

    @property
    def type(self) -> FilamentMonitorType:
        """Type of this filament monitor"""
        return self._type

    def _update_from_json(self, **kwargs) -> 'FilamentMonitorBase':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(FilamentMonitorBase, self)._update_from_json(**kwargs)
        self._type = FilamentMonitorType(kwargs.get('type', FilamentMonitorType.Unknown))
        return self
