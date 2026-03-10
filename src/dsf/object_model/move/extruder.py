from typing import Union

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
        self._acceleration: float = 500
        # Motor current (in mA)
        self._current: int = 0
        # Assigned driver
        self._driver = None
        # Extrusion factor to use (0..1 or greater)
        self._factor: float = 1
        # Name of the currently loaded filament
        self._filament: str = ""
        # Diameter of the corresponding filament (in mm)
        self._filament_diameter: float = 1.75
        # Motor jerk (in mm/s)
        self._jerk: float = 15
        # Microstepping configuration
        self._microstepping: MicroStepping = MicroStepping()
        # Nonlinear extrusion parameters (see M592)
        self._nonlinear: ExtruderNonlinear = ExtruderNonlinear()
        # Percentage applied to the motor current (0..100)
        self._percent_current: int = 100
        # Percentage applied to the motor current during standstill (0..100 or null if not supported)
        self._percent_stst_current: Union[int, None] = None
        # Whether or not the extruder is currently using phase stepping
        self._phase_step: Union[bool, None] = None
        # Extruder position (in mm)
        self._position: float = 0
        # Pressure advance
        self._pressure_advance: float = 0
        # Motor jerk during the current print only (in mm/s)
        self._printing_jerk: float = 15
        # Raw extruder position as commanded by the slicer without extrusion factor applied (in mm)
        self._raw_position: float = 0
        # Maximum speed (in mm/s)
        self._speed: float = 100
        # Number of microsteps per mm
        self._steps_per_mm: float = 420

    @property
    def acceleration(self) -> float:
        """Acceleration of this extruder (in mm/s^2)"""
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = float(value)

    @property
    def current(self) -> int:
        """Motor current (in mA)"""
        return self._current

    @current.setter
    def current(self, value):
        self._current = int(value)

    @property
    def factor(self) -> float:
        """Extrusion factor to use (0..1 or greater)"""
        return self._factor

    @factor.setter
    def factor(self, value):
        self._factor = float(value)

    @property
    def filament(self) -> str:
        """Name of the currently loaded filament"""
        return self._filament

    @filament.setter
    def filament(self, value):
        self._filament = str(value)

    @property
    def filament_diameter(self) -> float:
        """Diameter of the corresponding filament (in mm)"""
        return self._filament_diameter

    @filament_diameter.setter
    def filament_diameter(self, value):
        self._filament_diameter = float(value)

    @property
    def jerk(self) -> float:
        """Motor jerk (in mm/s)"""
        return self._jerk

    @jerk.setter
    def jerk(self, value):
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
    def percent_current(self, value):
        self._percent_current = int(value)

    @property
    def percent_stst_current(self) -> Union[int, None]:
        """Percentage applied to the motor current during standstill (0..100 or null if not supported)"""
        return self._percent_stst_current

    @percent_stst_current.setter
    def percent_stst_current(self, value):
        self._percent_stst_current = int(value) if value is not None else None

    @property
    def phase_stepping(self) -> Union[bool, None]:
        """Whether or not the axis is currently using phase stepping"""
        return self._phase_stepping

    @phase_stepping.setter
    def phase_stepping(self, value: Union[bool, None]):
        self._phase_stepping = bool(value) if value is not None else None

    @property
    def position(self) -> float:
        """Extruder position (in mm)"""
        return self._position

    @position.setter
    def position(self, value):
        self._position = float(value)

    @property
    def pressure_advance(self) -> float:
        """Pressure advance"""
        return self._pressure_advance

    @pressure_advance.setter
    def pressure_advance(self, value):
        self._pressure_advance = float(value)

    @property
    def printing_jerk(self) -> Union[float, None]:
        """Motor jerk during the current print only (in mm/s)"""
        return self._printing_jerk

    @printing_jerk.setter
    def printing_jerk(self, value):
        self._printing_jerk = float(value)

    @property
    def raw_position(self) -> float:
        """Raw extruder position as commanded by the slicer without extrusion factor applied (in mm)"""
        return self._raw_position

    @raw_position.setter
    def raw_position(self, value):
        self._raw_position = float(value)

    @property
    def speed(self) -> float:
        """Maximum speed (in mm/s)"""
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = float(value)

    @property
    def steps_per_mm(self) -> float:
        """Number of microsteps per mm"""
        return self._steps_per_mm

    @steps_per_mm.setter
    def steps_per_mm(self, value):
        self._steps_per_mm = float(value)
