from .filament_monitor_base import FilamentMonitorBase
from .filament_monitor_type import FilamentMonitorType
from .utils import get_filament_monitor


class FilamentMonitor(FilamentMonitorBase):
    """Information about a filament monitor"""

    def __init__(self, type_=FilamentMonitorType.Unknown):
        super(FilamentMonitor, self).__init__(type_)

    def _update_from_json(self, **kwargs) -> 'FilamentMonitorBase':
        """Override ObjectModel._update_from_json to return the FilamentMonitor type matching the given type"""
        super(FilamentMonitor, self)._update_from_json(**kwargs)
        type_ = kwargs.get('type_', FilamentMonitorType.Unknown)
        new_filament_monitor_type = FilamentMonitorType(type_)
        if new_filament_monitor_type != self.type:
            new_filament_monitor_instance = get_filament_monitor(new_filament_monitor_type)
            return new_filament_monitor_instance.from_json(kwargs)
        return self
