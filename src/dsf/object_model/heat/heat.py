from typing import List

from .heater import Heater
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
        self._heaters = []

    @property
    def bed_heaters(self) -> List[int]:
        """List of configured bed heaters (indices)
        Items may be -1 if unconfigured"""
        return self._bed_heaters

    @property
    def chamber_heaters(self) -> List[int]:
        """List of configured chamber heaters (indices)
        Items may be -1 if unconfigured"""
        return self._chamber_heaters

    @property
    def cold_extrude_temperature(self) -> float:
        """Minimum required temperature for extrusion moves (in C)"""
        return self._cold_extrude_temperature

    @cold_extrude_temperature.setter
    def cold_extrude_temperature(self, value: float = 160):
        self._cold_extrude_temperature = float(value) if value is not None else 160

    @property
    def cold_retract_temperature(self) -> float:
        """Minimum required temperature for retraction moves (in C)"""
        return self._cold_retract_temperature

    @cold_retract_temperature.setter
    def cold_retract_temperature(self, value: float = 90):
        self._cold_retract_temperature = float(value) if value is not None else 90

    @property
    def heaters(self) -> List[Heater]:
        """List of configured heaters"""
        return self._heaters

    def _update_from_json(self, **kwargs) -> 'Heat':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(Heat, self)._update_from_json(**kwargs)
        self._bed_heaters = [int(heater) for heater in kwargs.get('bedHeaters', [])]
        self._chamber_heaters = [int(heater) for heater in kwargs.get('chamberHeaters', [])]
        self._heaters = [Heater.from_json(heater) for heater in kwargs.get('heaters', [])]
        return self
