import dateutil.parser as dp
from datetime import datetime
from typing import Union

from .cpu import CPU
from .memory import Memory
from .dsf.dsf import DSF
from ..model_object import ModelObject


class SBC(ModelObject):
    """Information about the SBC in SBC mode"""

    def __init__(self):
        super().__init__()
        self._app_armor = False
        self._cpu = CPU()
        self._distribution = None
        self._distribution_build_time = None
        self._dsf = DSF()
        self._memory = Memory()
        self._model = None
        self._serial = None
        self._uptime = None

    @property
    def app_armor(self) -> bool:
        """Indicates if AppArmor support is enabled.
        By default, AppArmor is required for plugin functionality"""
        return self._app_armor

    @app_armor.setter
    def app_armor(self, value):
        self._app_armor = bool(value)

    @property
    def cpu(self) -> CPU:
        """Information about the SBC's CPU"""
        return self._cpu

    @property
    def distribution(self) -> Union[str, None]:
        """Name and version of the system distribution or None if unknown"""
        return self._distribution

    @distribution.setter
    def distribution(self, value):
        self._distribution = str(value) if value is not None else None

    @property
    def distribution_build_time(self) -> Union[datetime, None]:
        """Build datetime of the system distribution or None if unknown"""
        return self._distribution_build_time

    @distribution_build_time.setter
    def distribution_build_time(self, value):
        if value is None or isinstance(value, datetime):
            self._distribution_build_time = value
        elif isinstance(value, str):  # Update from JSON
            self._distribution_build_time = dp.isoparse(value)
        else:
            raise TypeError(f"{__name__}.distribution_build_time must be of type datetime or None."
                            f"Got {type(value)}: {value}")

    @property
    def dsf(self) -> DSF:
        """Information about DSF running on the SBC"""
        return self._dsf

    @property
    def memory(self) -> Memory:
        """Information about the SBC's memory (RAM)"""
        return self._memory

    @property
    def model(self) -> Union[str, None]:
        """SBC model or None if unknown"""
        return self._model

    @model.setter
    def model(self, value):
        self._model = str(value) if value is not None else None

    @property
    def serial(self) -> Union[str, None]:
        """SBC serial or None if unknown"""
        return self._serial

    @serial.setter
    def serial(self, value):
        self._serial = str(value) if value is not None else None

    @property
    def uptime(self) -> Union[float, None]:
        """Uptime of the running system (in s) or None if unknown"""
        return self._uptime

    @uptime.setter
    def uptime(self, value):
        self._uptime = float(value) if value is not None else None
