from .driver_id import DriverId
from .extruder_non_linear import ExtruderNonlinear
from .microstepping import MicroStepping
from ..model_object import ModelObject
from ..utils import nullable_model_prop, model_prop


class Extruder(ModelObject):
    """Information about an extruder drive"""

    # Acceleration of this extruder (in mm/s^2)
    acceleration = model_prop("acceleration", float, 500.0)

    # Motor current (in mA)
    current = model_prop("current", int, 0)

    # Assigned driver
    driver = nullable_model_prop('driver', DriverId)

    # Extrusion factor to use (0..1 or greater)
    factor = model_prop("factor", float, 1.0)

    # Name of the currently loaded filament
    filament = model_prop("filament", str, "")

    # Diameter of the corresponding filament (in mm)
    filament_diameter = model_prop("filament_diameter", float, 1.75)

    # Motor jerk (in mm/s)
    jerk = model_prop("jerk", float, 15.0)

    # Microstepping configuration
    microstepping = model_prop("microstepping", MicroStepping)

    # Nonlinear extrusion parameters (see M592)
    nonlinear = model_prop("nonlinear", ExtruderNonlinear)

    # Percentage applied to the motor current (0..100)
    percent_current = model_prop("percent_current", int, 100)

    # Percentage applied to the motor current during standstill (0..100 or null if not supported)
    percent_stst_current = nullable_model_prop("percent_stst_current", int)

    # Whether or not the extruder is currently using phase stepping
    phase_stepping = nullable_model_prop("phase_stepping", bool)

    # Extruder position (in mm)
    position = model_prop("position", float, 0.0)

    # Pressure advance
    pressure_advance = model_prop("pressure_advance", float, 0.0)

    # Motor jerk during the current print only (in mm/s)
    printing_jerk = model_prop("printing_jerk", float, 15.0)

    # Raw extruder position as commanded by the slicer without extrusion factor applied (in mm)
    raw_position = model_prop("raw_position", float, 0.0)

    # Maximum speed (in mm/s)
    speed = model_prop("speed", float, 100.0)

    # Number of microsteps per mm
    steps_per_mm = model_prop("steps_per_mm", float, 420.0)

    def __init__(self):
        super().__init__()
