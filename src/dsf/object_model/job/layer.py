from typing import List

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
    def duration(self, value):
        self._duration = float(value) if value is not None else 0

    @property
    def filament(self) -> List[float]:
        """Actual amount of filament extruded during this layer (in mm)"""
        return self._filament

    @property
    def fraction_printed(self) -> float:
        """Fraction of the file printed during this layer (0..1)"""
        return self._fraction_printed

    @fraction_printed.setter
    def fraction_printed(self, value):
        self._fraction_printed = float(value) if value is not None else 0

    @property
    def height(self) -> int:
        """Height of the layer (in mm or 0 if unknown)"""
        return self._height

    @height.setter
    def height(self, value):
        self._height = int(value) if value is not None else 0

    @property
    def temperatures(self) -> List[float]:
        """Last heater temperatures (in C or null if unknown)"""
        return self._temperatures

    def _update_from_json(self, **kwargs) -> 'Layer':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(Layer, self)._update_from_json(**kwargs)
        self._filament = [float(f) for f in kwargs.get('filament', [])]
        self._temperatures = [float(t) if t is not None else None for t in kwargs.get('temperatures', [])]
        return self
