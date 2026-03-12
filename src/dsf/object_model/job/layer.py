from typing import List

from ..model_object import ModelObject


class Layer(ModelObject):
    """Information about a layer from a file being printed"""

    def __init__(self) -> None:
        super().__init__()
        # Duration of the layer (in s)
        self._duration: float = 0
        # Actual amount of filament extruded during this layer (in mm)
        self._filament: List[float] = []
        # Amount of total filament extruderd during this layer (in mm)
        self._filament_usage: float = 0
        # Fraction of the file printed during this layer (0..1)
        self._fraction_printed: float = 0
        # Height of the layer (in mm or 0 if unknown)
        self._height: int = 0
        # Last heater temperatures (in C or null if unknown)
        self._temperatures: List[float] = []

    @property
    def duration(self) -> float:
        """Duration of the layer (in s)"""
        return self._duration

    @duration.setter
    def duration(self, value: float | int | str):
        self._duration = float(value)

    @property
    def filament(self) -> List[float]:
        """Actual amount of filament extruded during this layer (in mm)"""
        return self._filament

    @property
    def filament_usage(self) -> float:
        """Amount of total filament extruderd during this layer (in mm)"""
        return self._filament_usage

    @filament_usage.setter
    def filament_usage(self, value: float | int | str):
        self._filament_usage = float(value)

    @property
    def fraction_printed(self) -> float:
        """Fraction of the file printed during this layer (0..1)"""
        return self._fraction_printed

    @fraction_printed.setter
    def fraction_printed(self, value: float | int | str):
        self._fraction_printed = float(value)

    @property
    def height(self) -> int:
        """Height of the layer (in mm or 0 if unknown)"""
        return self._height

    @height.setter
    def height(self, value: int | str):
        self._height = int(value)

    @property
    def temperatures(self) -> List[float]:
        """Last heater temperatures (in C or null if unknown)"""
        return self._temperatures
