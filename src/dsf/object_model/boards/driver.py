from .driver_settings import DriverSettings
from ..model_object import ModelObject


class Driver(ModelObject):
    """Information about a driver"""
    def __init(self):
        super(Driver, self).__init__()
        # Configured settings of the driver
        self._settings = DriverSettings()

    @property
    def settings(self) -> DriverSettings:
        """Configured settings of the driver"""
        return self._settings

    def _update_from_json(self, **kwargs) -> 'Driver':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(Driver, self)._update_from_json(**kwargs)
        self._settings = DriverSettings.from_json(kwargs.get('settings'))
        return self
