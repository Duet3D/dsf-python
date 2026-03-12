from ..model_object import ModelObject


class CPU(ModelObject):
    """Information about the SBC's CPU"""

    def __init__(self) -> None:
        super().__init__()
        self._avg_load: float | None = None
        self._hardware: str | None = None
        self._num_cores: int = 1
        self._temperature: float | None = None

    @property
    def avg_load(self) -> float | None:
        """Average CPU load (0..100%) or None if unknown"""
        return self._avg_load

    @avg_load.setter
    def avg_load(self, value: float | int | str | None):
        self._avg_load = float(value) if value is not None else None

    @property
    def hardware(self) -> str | None:
        """CPU hardware as reported by /proc/cpuinfo"""
        return self._hardware

    @hardware.setter
    def hardware(self, value: str | None):
        self._hardware = str(value) if value is not None else None

    @property
    def num_cores(self) -> int:
        """Number of CPU cores/threads (defaults to 1)"""
        return self._num_cores

    @num_cores.setter
    def num_cores(self, value: int | str):
        self._num_cores = int(value)

    @property
    def temperature(self) -> float | None:
        """Current CPU temperature (in degC) or None if unknown"""
        return self._temperature

    @temperature.setter
    def temperature(self, value: float | int | str | None):
        self._temperature = float(value) if value is not None else None
