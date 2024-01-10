from typing import Union

from ..model_object import ModelObject


class CPU(ModelObject):
    """Information about the SBC's CPU"""

    def __init__(self):
        super().__init__()
        self._avg_load = None
        self._hardware = None
        self._num_cores = 1
        self._temperature = None

    @property
    def avg_load(self) -> Union[float, None]:
        """Average CPU load (0..100%) or None if unknown"""
        return self._avg_load

    @avg_load.setter
    def avg_load(self, value):
        self._avg_load = float(value) if value is not None else None

    @property
    def hardware(self) -> Union[str, None]:
        """CPU hardware as reported by /proc/cpuinfo"""
        return self._hardware

    @hardware.setter
    def hardware(self, value):
        self._hardware = str(value) if value is not None else None

    @property
    def num_cores(self) -> int:
        """Number of CPU cores/threads (defaults to 1)"""
        return self._num_cores

    @num_cores.setter
    def num_cores(self, value):
        self._num_cores = int(value)

    @property
    def temperature(self) -> Union[float, None]:
        """Current CPU temperature (in degC) or None if unknown"""
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = float(value) if value is not None else None
