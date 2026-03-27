from typing import List

from .axis import Axis
from .current_move import CurrentMove
from .extruder import Extruder
from .keepout_zone import KeepoutZone
from .kinematics import Kinematics
from .input_shaping import InputShaping
from .motion_system import MotionSystem
from .move_calibration import MoveCalibration
from .move_compensation import MoveCompensation
from .motors_idle_control import MotorsIdleControl
from .move_queue_item import MoveQueueItem
from .move_rotation import MoveRotation
from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import model_prop, nullable_model_prop


class Move(ModelObject):
    """Information about the move subsystem"""

    # Value of the M201 T parameter. Only present in builds that support S-curve acceleration
    acceleration_time = nullable_model_prop('acceleration_time', float)

    # List of the configured axes
    axes = model_prop('axes', ModelCollection[Axis], ModelCollection(Axis))

    # Backlash distance multiplier
    backlash_factor = model_prop('backlash_factor', int, 10)

    # Information about the automatic calibration
    calibration = model_prop('calibration', MoveCalibration)

    # Information about the currently configured compensation options
    compensation = model_prop('compensation', MoveCompensation)

    # Information about the current move
    current_move = model_prop('current_move', CurrentMove)

    # List of configured extruders
    extruders = model_prop('extruders', ModelCollection[Extruder], ModelCollection(Extruder))

    # Idle current reduction parameters
    idle = model_prop('idle', MotorsIdleControl)

    # List of configured keep-out zones
    keepout = model_prop('keepout', ModelCollection[KeepoutZone], ModelCollection(KeepoutZone))

    # Configured kinematics options
    kinematics = model_prop('kinematics', Kinematics)

    # Limit axis positions by their minima and maxima
    limit_axes = model_prop('limit_axes', bool, True)

    # Indicates if standard moves are forbidden if the corresponding axis is not homed
    no_moves_before_homing = model_prop('no_moves_before_homing', bool, True)

    # List of configured motion systems
    motion_systems = model_prop('motion_systems', ModelCollection[MotionSystem], ModelCollection(MotionSystem))

    # Maximum acceleration allowed while printing (in mm/s^2)
    # deprecated, use motion_systems[].printing_acceleration instead
    printing_acceleration = model_prop('printing_acceleration', float, 10000)

    # List of move queue items (DDA rings)
    queue = model_prop('queue', ModelCollection[MoveQueueItem], ModelCollection(MoveQueueItem))

    # Parameters for centre rotation
    # deprecated, use motion_systems[].rotation instead
    rotation = model_prop('rotation', MoveRotation)

    # Parameters for input shaping
    shaping = model_prop('shaping', InputShaping)

    # Speed factor applied to every regular move (0.01..1 or greater)
    speed_factor = model_prop('speed_factor', float, 1)

    # Maximum acceleration allowed while travelling (in mm/s^2)
    # deprecated, use motion_systems[].travel_acceleration instead
    travel_acceleration = model_prop('travel_acceleration', float, 0)

    # Indicates if third-order S-curve acceleration is enabled
    s_curve_acceleration = model_prop('s_curve_acceleration', bool, False)

    # Virtual total extruder position
    # deprecated, use motion_systems[].virtual_e_pos instead
    virtual_e_pos = model_prop('virtual_e_pos', float, 0)

    # Index of the currently selected workplace
    # deprecated, use motion_systems[].workplace_number instead
    workplace_number = model_prop('workplace_number', int, 0)

    def __init__(self):
        super().__init__()