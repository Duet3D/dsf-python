from enum import Enum
from typing import Union

from .move_calibration import MoveDeviations
from .probe_grid import ProbeGrid
from .skew import Skew
from ..model_object import ModelObject
from ..utils import wrap_model_property


class MoveCompensationType(str, Enum):
    """Supported compensation types"""

    # No compensation
    none = "none"

    # Mesh compensation
    mesh = "mesh"


class MoveCompensation(ModelObject):
    """Information about the configured compensation options"""

    # Grid settings of the loaded heightmap or null if no heightmap is loaded
    live_grid = wrap_model_property('live_grid', ProbeGrid)
    # Deviations of the mesh grid or null if not applicable
    mesh_deviation = wrap_model_property('mesh_deviation', MoveDeviations)

    def __init__(self):
        super().__init__()
        # Effective height before the bed compensation is turned off (in mm) or null if not configured
        self._fade_height = None
        # Full path to the currently used height map file or null if none is in use
        self._file = ""
        # Grid settings of the loaded heightmap or null if no heightmap is loaded
        self._live_grid = None
        # Deviations of the mesh grid or null if not applicable
        self._mesh_deviation = None
        # Probe grid settings as defined by M557
        self._probe_grid = ProbeGrid()
        # Information about the configured orthogonal axis parameters
        self._skew = Skew()
        # Type of the compensation in use
        self._type = MoveCompensationType.none

    @property
    def fade_height(self) -> Union[float, None]:
        """Effective height before the bed compensation is turned off (in mm) or null if not configured"""
        return self._fade_height

    @fade_height.setter
    def fade_height(self, value):
        self._fade_height = float(value) if value is not None else None

    @property
    def file(self) -> Union[str, None]:
        """Full path to the currently used height map file or null if none is in use"""
        return self._file

    @file.setter
    def file(self, value):
        self._file = str(value) if value is not None else None

    @property
    def probe_grid(self) -> ProbeGrid:
        """Probe grid settings as defined by M557"""
        return self._probe_grid

    @property
    def skew(self) -> Skew:
        """Information about the configured orthogonal axis parameters"""
        return self._skew

    @property
    def type(self) -> MoveCompensationType:
        """Type of the compensation in use"""
        return self._type

    @type.setter
    def type(self, value):
        if value is None or value == "":
            self._type = MoveCompensationType.none
        elif isinstance(value, MoveCompensationType):
            self._type = value
        elif isinstance(value, str):
            self._type = MoveCompensationType(value)
        else:
            raise TypeError(f"{__name__}.type must be of type MoveCompensationType. Got {type(value)}: {value}")
