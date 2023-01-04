from __future__ import annotations

from .heater import Heater
from ..model_collection import ModelCollection
from ..model_object import ModelObject


class Heat(ModelObject):
    """Information about the heat subsystem"""

    def __init__(self):
        super().__init__()
        # List of configured bed heaters (indices)
        self._bed_heaters = []
        # List of configured chamber heaters (indices)
        self._chamber_heaters = []
        # Minimum required temperature for extrusion moves (in C)
        self._cold_extrude_temperature = 160
        # Minimum required temperature for retraction moves (in C)
        self._cold_retract_temperature = 90
        # List of configured heaters
        self._heaters = ModelCollection(Heater)

    @property
    def bed_heaters(self) -> list[int]:
        """List of configured bed heaters (indices)
        Items may be -1 if unconfigured"""
        return self._bed_heaters

    @property
    def chamber_heaters(self) -> list[int]:
        """List of configured chamber heaters (indices)
        Items may be -1 if unconfigured"""
        return self._chamber_heaters

    @property
    def cold_extrude_temperature(self) -> float:
        """Minimum required temperature for extrusion moves (in C)"""
        return self._cold_extrude_temperature

    @cold_extrude_temperature.setter
    def cold_extrude_temperature(self, value: float):
        self._cold_extrude_temperature = float(value)

    @property
    def cold_retract_temperature(self) -> float:
        """Minimum required temperature for retraction moves (in C)"""
        return self._cold_retract_temperature

    @cold_retract_temperature.setter
    def cold_retract_temperature(self, value: float):
        self._cold_retract_temperature = float(value)

    @property
    def heaters(self) -> list[Heater]:
        """List of configured heaters"""
        return self._heaters
