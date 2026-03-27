from ..model_object import ModelObject
from ..model_collection import ModelCollection
from ..utils import model_prop, nullable_model_prop

from .current_move import CurrentMove
from .move_rotation import MoveRotation
from ..state.restore_point import RestorePoint

class MotionSystem(ModelObject):
    """Information about a motion system"""

    # Information about the current move
    current_move = model_prop("current_move", CurrentMove)

    # Number of the current object being printed or null if not printing
    current_object = nullable_model_prop("current_object", int)

    # Number of the currently selected tool or -1 if no tool is selected
    current_tool = model_prop("current_tool", int, -1)

    # Number of the next tool to be selected
    next_tool = model_prop("next_tool", int, -1)

    # Number of the previous tool
    previous_tool = model_prop("previous_tool", int, -1)

    # Maximum acceleration allowed while printing (in mm/s^2)
    max_print_acceleration = model_prop("max_print_acceleration", float, 10000.0)

    # List of restore points
    restore_points = model_prop("restore_points", ModelCollection[RestorePoint], ModelCollection(RestorePoint))

    # Parameters for centre rotation
    rotation = model_prop("rotation", MoveRotation)

    # Speed factor applied to every regular move (0.01..1 or greater)
    speed_factor = model_prop("speed_factor", float, 1.0)

    # Maximum acceleration allowed while traveling (in mm/s^2)
    travel_acceleration = model_prop("travel_acceleration", float, 10000.0)

    # User coordinates of the motion system
    user_coordinates = model_prop("user_coordinates", ModelCollection[float], ModelCollection(float))

    # Virtual tool extruder position
    virtual_e_pos = model_prop("virtual_e_pos", float, 0.0)

    # Index of the currently selected workplace
    workplace_number = model_prop("workplace_number", int)

    def __init__(self):
        super().__init__()
