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
