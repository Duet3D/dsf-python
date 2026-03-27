from enum import Enum
from typing import Union

from .move_calibration import MoveDeviations
from .probe_grid import ProbeGrid
from .skew import Skew
from ..model_object import ModelObject
from ..utils import nullable_model_prop, model_prop


class MoveCompensationType(str, Enum):
    """Supported compensation types"""

    # No compensation
    none = "none"

    # Mesh compensation
    mesh = "mesh"


class MoveCompensation(ModelObject):
    """Information about the configured compensation options"""

    # Effective height before the bed compensation is turned off (in mm) or null if not configured
    fade_height = nullable_model_prop('fade_height', float)
    
    # Full path to the currently used height map file or null if none is in use
    file = nullable_model_prop('file', str)

    # Grid settings of the loaded heightmap or null if no heightmap is loaded
    live_grid = nullable_model_prop('live_grid', ProbeGrid)

    # Deviations of the mesh grid or null if not applicable
    mesh_deviation = nullable_model_prop('mesh_deviation', MoveDeviations)

    # Probe grid settings as defined by M557
    probe_grid = model_prop('probe_grid', ProbeGrid)

    # Information about the configured orthogonal axis parameters
    skew = model_prop('skew', Skew)

    # Type of the compensation in use
    type = model_prop('type', MoveCompensationType, MoveCompensationType.none)

    def __init__(self):
        super().__init__()
