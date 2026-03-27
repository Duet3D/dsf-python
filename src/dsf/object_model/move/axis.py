from enum import Enum
from typing import List, Optional

from .driver_id import DriverId
from .microstepping import MicroStepping
from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import model_prop, nullable_model_prop


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

    # Acceleration of this axis (in mm/s^2)
    acceleration = model_prop("acceleration", float, 0.0)

    # Babystep amount (in mm)
    babystep = model_prop("babystep", float, 0.0)

    # Configured backlash of this axis (in mm)
    backlash = model_prop("backlash", float, 0.0)

    # Motor current (in mA)
    current = model_prop("current", int, 0)

    # List of the assigned drivers
    drivers = model_prop("drivers", ModelCollection[DriverId], ModelCollection(DriverId))

    # Whether the axis is homed
    homed = model_prop("homed", bool, False)

    # Motor jerk (in mm/min)
    jerk = model_prop("jerk", float, 15.0)

    # Letter of this axis
    letter = model_prop("letter", AxisLetter, AxisLetter.none)

    # Current machine position (in mm) or None if unknown/unset
    machine_position = nullable_model_prop("machine_position", float)

    # Maximum travel of this axis (in mm)
    max = model_prop("max", float, 200.0)

    # Whether the axis maximum was probed
    max_probed = model_prop("max_probed", bool, False)

    # Microstepping configuration
    microstepping = model_prop("microstepping", MicroStepping)

    # Minimum travel of this axis (in mm)
    min = model_prop("min", float, 0.0)

    # Whether the axis minimum was probed
    min_probed = model_prop("min_probed", bool, False)

    # Percentage applied to the motor current (0..100)
    percent_current = model_prop("percent_current", int, 100)

    # Percentage applied to the motor current during standstill (0..100 or None if not supported)
    percent_stst_current = nullable_model_prop("percent_stst_current", int)

    # Whether or not the axis is currently using phase stepping
    phase_stepping = nullable_model_prop("phase_stepping", bool)

    # Motor jerk during the current print only (in mm/s)
    printing_jerk = model_prop("printing_jerk", float, 15.0)

    # Reduced accelerations used by Z probing and stall homing moves (in mm/s^2)
    reduced_acceleration = model_prop("reduced_acceleration", float, 0.0)

    # Maximum speed (in mm/min)
    speed = model_prop("speed", float, 100.0)

    # Number of microsteps per mm
    steps_per_mm = model_prop("steps_per_mm", float, 80.0)

    # Current step position of the axis (in steps)
    step_pos = model_prop("step_pos", int, 0)

    # Current user position (in mm) or None if unknown
    user_position = nullable_model_prop("user_position", float)

    # Whether the axis is visible
    visible = model_prop("visible", bool, True)

    # Offsets of this axis for each workplace (in mm)
    workplace_offsets = model_prop("workplace_offsets", ModelCollection[float], ModelCollection(float))

    def __init__(self):
        super().__init__()