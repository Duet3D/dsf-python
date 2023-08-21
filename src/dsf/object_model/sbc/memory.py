from typing import Union

from ..model_object import ModelObject


class Memory(ModelObject):
    """Information about the SBC's memory (RAM)"""

    def __init__(self):
        super().__init__()
        self._available = None
        self._total = None

    @property
    def available(self) -> Union[int, None]:
        """Available memory (in bytes)"""
        return self._available

    @available.setter
    def available(self, value):
        self._available = int(value) if value is not None else None

    @property
    def total(self) -> Union[int, None]:
        """Total memory (in bytes)"""
        return self._total

    @total.setter
    def total(self, value):
        self._total = int(value) if value is not None else None
