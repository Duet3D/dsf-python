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
