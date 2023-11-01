from __future__ import annotations

from .driver_id import DriverId
from .extruder_non_linear import ExtruderNonlinear
from .microstepping import MicroStepping
from ..model_object import ModelObject
from ..utils import wrap_model_property


class Extruder(ModelObject):
    """Information about an extruder drive"""

    # Assigned driver
    driver = wrap_model_property('driver', DriverId)

    def __init__(self):
        super().__init__()
        # Acceleration of this extruder (in mm/s^2)
        self._acceleration = 500
        # Motor current (in mA)
        self._current = 0
        # Assigned driver
        self._driver = None
        # Name of the currently loaded filament
        self._filament = ""
        # Extrusion factor to use (0..1 or greater)
        self._factor = 1
        # Motor jerk (in mm/s)
        self._jerk = 15
        # Microstepping configuration
        self._microstepping = MicroStepping()
        # Nonlinear extrusion parameters (see M592)
        self._nonlinear = ExtruderNonlinear()
        # Percentage applied to the motor current (0..100)
        self._percent_current = 100
        # Percentage applied to the motor current during standstill (0..100 or None if not supported)
        self._percent_stst_current = None
        # Extruder position (in mm)
        self._position = 0
        # Pressure advance
        self._pressure_advance = 0
        # Raw extruder position as commanded by the slicer without extrusion factor applied (in mm)
        self._raw_position = 0
        # Maximum speed (in mm/s)
        self._speed = 100
        # Number of microsteps per mm
        self._steps_per_mm = 420

    @property
    def acceleration(self) -> float:
        """Acceleration of this extruder (in mm/s^2)"""
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value: float):
        self._acceleration = float(value)

    @property
    def current(self) -> int:
        """Motor current (in mA)"""
        return self._current

    @current.setter
    def current(self, value: int):
        self._current = int(value)

    @property
    def filament(self) -> str:
        """Name of the currently loaded filament"""
        return self._filament

    @filament.setter
    def filament(self, value: str):
        self._filament = str(value)

    @property
    def factor(self) -> float:
        """Extrusion factor to use (0..1 or greater)"""
        return self._factor

    @factor.setter
    def factor(self, value: float):
        self._factor = float(value)

    @property
    def jerk(self) -> float:
        """Motor jerk (in mm/s)"""
        return self._jerk

    @jerk.setter
    def jerk(self, value: float):
        self._jerk = float(value)

    @property
    def microstepping(self) -> MicroStepping:
        """Microstepping configuration"""
        return self._microstepping

    @property
    def nonlinear(self) -> ExtruderNonlinear:
        """Nonlinear extrusion parameters (see M592)"""
        return self._nonlinear

    @property
    def percent_current(self) -> int:
        """Percentage applied to the motor current (0..100)"""
        return self._percent_current

    @percent_current.setter
    def percent_current(self, value: int):
        self._percent_current = int(value)

    @property
    def percent_stst_current(self) -> int | None:
        """Percentage applied to the motor current during standstill (0..100 or None if not supported)"""
        return self._percent_stst_current

    @percent_stst_current.setter
    def percent_stst_current(self, value: int | None = None):
        self._percent_stst_current = int(value) if value is not None else None

    @property
    def position(self) -> float:
        """Extruder position (in mm)"""
        return self._position

    @position.setter
    def position(self, value: float):
        self._position = float(value)

    @property
    def pressure_advance(self) -> float:
        """Pressure advance"""
        return self._pressure_advance

    @pressure_advance.setter
    def pressure_advance(self, value: float):
        self._pressure_advance = float(value)

    @property
    def raw_position(self) -> float:
        """Raw extruder position as commanded by the slicer without extrusion factor applied (in mm)"""
        return self._raw_position

    @raw_position.setter
    def raw_position(self, value: float):
        self._raw_position = float(value)

    @property
    def speed(self) -> float:
        """Maximum speed (in mm/s)"""
        return self._speed

    @speed.setter
    def speed(self, value: float):
        self._speed = float(value)

    @property
    def steps_per_mm(self) -> float:
        """Number of microsteps per mm"""
        return self._steps_per_mm

    @steps_per_mm.setter
    def steps_per_mm(self, value: float):
        self._steps_per_mm = float(value)
