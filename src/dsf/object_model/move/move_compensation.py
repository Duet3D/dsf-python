from enum import Enum
from typing import Union

from .move_calibration import MoveDeviations
from .probe_grid import ProbeGrid
from .skew import Skew
from ..model_object import ModelObject


class MoveCompensationType(str, Enum):
    """Supported compensation types"""

    # No compensation
    none = "none"

    # Mesh compensation
    mesh = "mesh"


class MoveCompensation(ModelObject):
    """Information about the configured compensation options"""

    def __init__(self):
        super().__init__()
        # Effective height before the bed compensation is turned off (in mm) or null if not configured
        self._fade_height = None
        # Full path to the currently used height map file or null if none is in use
        self._file = ""
        # Grid settings of the loaded heightmap or null if no heightmap is loaded
        self._live_grid = ProbeGrid()
        # Deviations of the mesh grid or null if not applicable
        self._mesh_deviation = MoveDeviations()
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
    def live_grid(self) -> Union[ProbeGrid, None]:
        """Grid settings of the loaded heightmap or null if no heightmap is loaded"""
        return self._live_grid

    @live_grid.setter
    def live_grid(self, value):
        if isinstance(value, ProbeGrid) or value is None:
            self._live_grid = value
        elif isinstance(value, dict):  # Update from JSON
            self._live_grid = ProbeGrid.from_json(value)
        else:
            raise TypeError(f"{__name__}.live_grid must be of type ProbeGrid. Got {type(value)}: {value}")

    @property
    def mesh_deviation(self) -> MoveDeviations:
        """Deviations of the mesh grid or null if not applicable"""
        return self._mesh_deviation

    @mesh_deviation.setter
    def mesh_deviation(self, value):
        if not isinstance(value, MoveDeviations) or value is None:
            self._mesh_deviation = value
        else:
            raise TypeError(f"{__name__}.mesh_deviation must be of type MoveDeviations. Got {type(value)}: {value}")

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

    def _update_from_json(self, **kwargs) -> 'MoveCompensation':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(MoveCompensation, self)._update_from_json(**kwargs)
        self._probe_grid = ProbeGrid.from_json(kwargs.get('probeGrid'))
        self._skew = Skew.from_json(kwargs.get('skew'))
        return self
