from enum import Enum
from typing import Any, List, Sequence, Union

from .driver_id import DriverId
from .microstepping import MicroStepping
from ..model_collection import ModelCollection
from ..model_object import ModelObject


class AxisLetter(str, Enum):
    """List of supported axis letters"""

    X = 'X'
    Y = 'Y'
    Z = 'Z'
    U = 'U'
    V = 'V'
    W = 'W'
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    a = 'a'
    b = 'b'
    c = 'c'
    d = 'd'
    e = 'e'
    f = 'f'
    g = 'g'
    h = 'h'
    i = 'i'
    j = 'j'
    k = 'k'
    l = 'l'
    m = 'm'
    n = 'n'
    o = 'o'
    p = 'p'
    q = 'q'
    r = 'r'
    s = 's'
    t = 't'
    u = 'u'
    v = 'v'
    w = 'w'
    x = 'x'
    y = 'y'
    z = 'z'
    none = ''


class Axis(ModelObject):
    """Information about a configured axis"""

    def __init__(self):
        super().__init__()
        # Acceleration of this axis (in mm/s^2)
        self._acceleration: float = 0
        # Babystep amount (in mm)
        self._babystep: float = 0
        # Configured backlash of this axis (in mm)
        self._backlash: float = 0
        # Motor current (in mA)
        self._current: int = 0
        # List of the assigned drivers
        self._drivers = ModelCollection(DriverId)
        # Whether the axis is homed
        self._homed: bool = False
        # Motor jerk (in mm/min)
        self._jerk: float = 15
        # Letter of this axis
        self._letter: AxisLetter = AxisLetter.none
        # Current machine position (in mm) or None if unknown/unset
        self._machine_position: Union[float, None] = None
        # Maximum travel of this axis (in mm)
        self._max: float = 200
        # Whether the axis maximum was probed
        self._max_probed: bool = False
        # Microstepping configuration
        self._microstepping: MicroStepping = MicroStepping()
        # Minimum travel of this axis (in mm)
        self._min: float = 0
        # Whether the axis minimum was probed
        self._min_probed: bool = False
        # Percentage applied to the motor current (0..100)
        self._percent_current: int = 100
        # Percentage applied to the motor current during standstill (0..100 or None if not supported)
        self._percent_stst_current: Union[int, None] = None
        # Whether or not the axis is currently using phase stepping
        self._phase_stepping: Union[bool, None] = None
        # Motor jerk during the current print only (in mm/s)
        self._printing_jerk: float = 15
        # Reduced accelerations used by Z probing and stall homing moves (in mm/s^2)
        self._reduced_acceleration: float = 0
        # Maximum speed (in mm/min)
        self._speed: float = 100
        # Number of microsteps per mm
        self._steps_per_mm: float = 80
        # Current step position of the axis (in steps)
        self._step_pos: int = 0
        # Current user position (in mm) or None if unknown
        self._user_position: Union[float, None] = None
        # Whether the axis is visible
        self._visible: bool = True
        # Offsets of this axis for each workplace (in mm)
        self._workplace_offsets: List[float] = []

    @property
    def acceleration(self) -> float:
        """Acceleration of this axis (in mm/s^2)"""
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value: Any):
        self._acceleration = float(value)

    @property
    def babystep(self) -> float:
        """Babystep amount (in mm)"""
        return self._babystep

    @babystep.setter
    def babystep(self, value: Any):
        self._babystep = float(value)

    @property
    def backlash(self) -> float:
        """Configured backlash of this axis (in mm)"""
        return self._backlash

    @backlash.setter
    def backlash(self, value: Any):
        self._backlash = float(value)

    @property
    def current(self) -> int:
        """Motor current (in mA)"""
        return self._current

    @current.setter
    def current(self, value: Any):
        self._current = int(value)

    @property
    def drivers(self) -> Sequence[DriverId | None]:
        """List of the assigned drivers"""
        return self._drivers

    @property
    def homed(self) -> bool:
        """Whether the axis is homed"""
        return self._homed

    @homed.setter
    def homed(self, value: Any):
        self._homed = bool(value)

    @property
    def jerk(self) -> float:
        """Motor jerk (in mm/min)"""
        return self._jerk

    @jerk.setter
    def jerk(self, value: Any):
        self._jerk = float(value)

    @property
    def letter(self) -> AxisLetter:
        """Letter of this axis"""
        return self._letter

    @letter.setter
    def letter(self, value: Any):
        if isinstance(value, AxisLetter):
            self._letter = value
        elif isinstance(value, str):
            self._letter = AxisLetter(value)
        else:
            raise TypeError(f"{__name__}.letter must be of type AxisLetter. Got {type(value)}: {value}")

    @property
    def machine_position(self) -> Union[float, None]:
        """Current machine position (in mm) or None if unknown/unset
        This value reflects the machine position of the move being performed
        or of the last one if the machine is not moving"""
        return self._machine_position

    @machine_position.setter
    def machine_position(self, value: Any):
        self._machine_position = float(value) if value is not None else None

    @property
    def max(self) -> float:
        """Maximum travel of this axis (in mm)"""
        return self._max

    @max.setter
    def max(self, value: Any):
        self._max = float(value)

    @property
    def max_probed(self) -> bool:
        """Whether the axis maximum was probed"""
        return self._max_probed

    @max_probed.setter
    def max_probed(self, value: Any):
        self._max_probed = bool(value)

    @property
    def microstepping(self) -> MicroStepping:
        """Microstepping configuration"""
        return self._microstepping

    @property
    def min(self) -> float:
        """Minimum travel of this axis (in mm)"""
        return self._min

    @min.setter
    def min(self, value: Any):
        self._min = float(value)

    @property
    def min_probed(self) -> bool:
        """Whether the axis minimum was probed"""
        return self._min_probed

    @min_probed.setter
    def min_probed(self, value: Any):
        self._min_probed = bool(value)

    @property
    def percent_current(self) -> int:
        """Percentage applied to the motor current (0..100)"""
        return self._percent_current

    @percent_current.setter
    def percent_current(self, value: Any):
        self._percent_current = int(value)

    @property
    def percent_stst_current(self) -> Union[int, None]:
        """Percentage applied to the motor current during standstill (0..100 or None if not supported)"""
        return self._percent_stst_current

    @percent_stst_current.setter
    def percent_stst_current(self, value: Any):
        self._percent_stst_current = int(value) if value is not None else None

    @property
    def phase_stepping(self) -> Union[bool, None]:
        """Whether or not the axis is currently using phase stepping"""
        return self._phase_stepping

    @phase_stepping.setter
    def phase_stepping(self, value: Union[bool, None]):
        self._phase_stepping = bool(value) if value is not None else None

    @property
    def printing_jerk(self) -> float:
        """Motor jerk during the current print only (in mm/s)"""
        return self._printing_jerk

    @printing_jerk.setter
    def printing_jerk(self, value: Any):
        self._printing_jerk = float(value)

    @property
    def reduced_acceleration(self) -> float:
        """Reduced accelerations used by Z probing and stall homing moves (in mm/s^2)"""
        return self._reduced_acceleration

    @reduced_acceleration.setter
    def reduced_acceleration(self, value: Any):
        self._reduced_acceleration = float(value)

    @property
    def speed(self) -> float:
        """Maximum speed (in mm/min)"""
        return self._speed

    @speed.setter
    def speed(self, value: Any):
        self._speed = float(value)

    @property
    def steps_per_mm(self) -> float:
        """Number of microsteps per mm"""
        return self._steps_per_mm

    @steps_per_mm.setter
    def steps_per_mm(self, value: Any):
        self._steps_per_mm = float(value)

    @property
    def step_pos(self) -> int:
        """Current step position of the axis (in steps)"""
        return self._step_pos

    @step_pos.setter
    def step_pos(self, value: int):
        self._step_pos = int(value)

    @property
    def user_position(self) -> Union[float, None]:
        """Current user position (in mm) or None if unknown
        This value reflects the target position of the last move fed into the look-ahead buffer"""
        return self._user_position

    @user_position.setter
    def user_position(self, value: Any):
        self._user_position = float(value) if value is not None else None

    @property
    def visible(self) -> bool:
        """Whether the axis is visible"""
        return self._visible

    @visible.setter
    def visible(self, value: Any):
        self._visible = bool(value)

    @property
    def workplace_offsets(self) -> List[float]:
        """Offsets of this axis for each workplace (in mm)"""
        return self._workplace_offsets
