from ..model_object import ModelObject
from ..utils import model_prop


class ToolRetraction(ModelObject):
    """Tool retraction parameters"""

    # Amount of additional filament to extrude when undoing a retraction (in mm)
    extra_restart = model_prop("extra_restart", float, 0)

    # Retraction length (in mm)
    length = model_prop("length", float, 0)

    # Retraction speed (in mm/s)
    speed = model_prop("speed", float, 0)

    # Unretract speed (in mm/s)
    unretract_speed = model_prop("unretract_speed", float, 0)

    # Amount of Z lift after doing a retraction (in mm)
    z_hop = model_prop("z_hop", float, 0)

    def __init__(self):
        super().__init__()        
