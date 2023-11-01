from __future__ import annotations

from ..model_object import ModelObject


class Layer(ModelObject):
    """Information about a layer from a file being printed"""

    def __init__(self):
        super().__init__()
        # Duration of the layer (in s)
        self._duration = 0
        # Actual amount of filament extruded during this layer (in mm)
        self._filament = []
        # Fraction of the file printed during this layer (0..1)
        self._fraction_printed = 0
        # Height of the layer (in mm or 0 if unknown)
        self._height = 0
        # Last heater temperatures (in C or null if unknown)
        self._temperatures = []

    @property
    def duration(self) -> float:
        """Duration of the layer (in s)"""
        return self._duration

    @duration.setter
    def duration(self, value: float):
        self._duration = float(value)

    @property
    def filament(self) -> list[float]:
        """Actual amount of filament extruded during this layer (in mm)"""
        return self._filament

    @property
    def fraction_printed(self) -> float:
        """Fraction of the file printed during this layer (0..1)"""
        return self._fraction_printed

    @fraction_printed.setter
    def fraction_printed(self, value: float):
        self._fraction_printed = float(value)

    @property
    def height(self) -> int:
        """Height of the layer (in mm or 0 if unknown)"""
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = int(value)

    @property
    def temperatures(self) -> list[float]:
        """Last heater temperatures (in C or null if unknown)"""
        return self._temperatures
