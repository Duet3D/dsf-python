from .stall_detect_settings import StallDetectSettings
from ..model_object import ModelObject


class DriverSettings(ModelObject):
    """Information about driver settings"""

    def __init__(self):
        super(DriverSettings, self).__init__()
        # Whether the drive goes forwards
        self._forwards = False
        # Stall detection settings
        self._stall_detect = StallDetectSettings()

    @property
    def forwards(self) -> bool:
        """Whether the drive goes forwards"""
        return self._forwards

    @forwards.setter
    def forwards(self, value: bool):
        self._forwards = bool(value)

    @property
    def stall_detect(self) -> StallDetectSettings:
        """Stall detection settings"""
        return self._stall_detect

    def _update_from_json(self, **kwargs) -> 'DriverSettings':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(DriverSettings, self)._update_from_json(**kwargs)
        self._stall_detect = StallDetectSettings.from_json(kwargs.get('stallDetect'))
        return self
