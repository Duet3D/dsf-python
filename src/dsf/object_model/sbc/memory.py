from ..model_object import ModelObject


class Memory(ModelObject):
    """Information about the SBC's memory (RAM)"""

    def __init__(self) -> None:
        super().__init__()
        self._available: int | None = None
        self._total: int | None = None

    @property
    def available(self) -> int | None:
        """Available memory (in bytes)"""
        return self._available

    @available.setter
    def available(self, value: int | str | None):
        self._available = int(value) if value is not None else None

    @property
    def total(self) -> int | None:
        """Total memory (in bytes)"""
        return self._total

    @total.setter
    def total(self, value: int | str | None):
        self._total = int(value) if value is not None else None
