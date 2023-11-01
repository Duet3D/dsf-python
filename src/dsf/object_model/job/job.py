from __future__ import annotations

from .build import Build
from .gcode_fileinfo import GCodeFileInfo
from .layer import Layer
from .times_left import TimesLeft
from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import wrap_model_property


class Job(ModelObject):
    """Information about the current job"""

    # Information about the current build or null if not available
    build = wrap_model_property('build', Build)
    # Information about the file being processed
    file = wrap_model_property('file', GCodeFileInfo)

    def __init__(self):
        super().__init__()
        # Information about the current build or null if not available
        self._build = None
        # Total active duration of the current job file (in s or null)
        self._duration = None
        # Information about the file being processed
        self._file = None
        # Current position in the file being processed (in bytes or null)
        self._file_position = None
        # Total duration of the last job (in s or null)
        self._last_duration = None
        # Indicates if the last file was aborted (unexpected cancellation)
        self._last_file_aborted = False
        # Indicates if the last file was cancelled (user cancelled)
        self._last_file_cancelled = False
        # Name of the last file processed or null if none
        self._last_file_name = None
        # Indicates if the last file processed was simulated
        self._last_file_simulated = False
        # Number of the current layer or null not available
        self._layer = None
        # Information about the past layers
        self._layers = ModelCollection(Layer)
        # Time elapsed since the last layer change (in s or null)
        self._layer_time = None
        # Total pause time since the job started
        self._pause_duration = None
        # Total extrusion amount without extrusion factors applied (in mm)
        self._raw_extrusion = None
        # Estimated times left
        self._times_left = TimesLeft()
        # Time needed to heat up the heaters (in s or null)
        self._warm_up_duration = None

    @property
    def duration(self) -> int | None:
        """Total active duration of the current job file (in s or null)"""
        return self._duration

    @duration.setter
    def duration(self, value: int | None = None):
        self._duration = int(value) if value is not None else None

    @property
    def file_position(self) -> int | None:
        """Current position in the file being processed (in bytes or null)"""
        return self._file_position

    @file_position.setter
    def file_position(self, value: int | None = None):
        self._file_position = int(value) if value is not None else None

    @property
    def last_duration(self) -> int | None:
        """Total duration of the last job (in s or null)"""
        return self._last_duration

    @last_duration.setter
    def last_duration(self, value: int | None = None):
        self._last_duration = int(value) if value is not None else None

    @property
    def last_file_aborted(self) -> bool:
        """Indicates if the last file was aborted (unexpected cancellation)"""
        return self._last_file_aborted

    @last_file_aborted.setter
    def last_file_aborted(self, value: bool):
        self._last_file_aborted = bool(value)

    @property
    def last_file_cancelled(self) -> bool:
        """Indicates if the last file was cancelled (user cancelled)"""
        return self._last_file_cancelled

    @last_file_cancelled.setter
    def last_file_cancelled(self, value: bool):
        self._last_file_cancelled = bool(value)

    @property
    def last_file_name(self) -> str | None:
        """Name of the last file processed or null if none"""
        return self._last_file_name

    @last_file_name.setter
    def last_file_name(self, value: str | None = None):
        self._last_file_name = str(value) if value is not None else None

    @property
    def last_file_simulated(self) -> bool:
        """Indicates if the last file processed was simulated
        This is not set if the file was aborted or cancelled"""
        return self._last_file_simulated

    @last_file_simulated.setter
    def last_file_simulated(self, value: bool):
        self._last_file_simulated = bool(value)

    @property
    def layer(self) -> int | None:
        """Number of the current layer or null not available"""
        return self._layer

    @layer.setter
    def layer(self, value: int | None = None):
        self._layer = int(value) if value is not None else None

    @property
    def layers(self) -> list[Layer]:
        """Information about the past layers
        See also Layer"""
        return self._layers

    @property
    def layer_time(self) -> float | None:
        """Time elapsed since the last layer change (in s or null)"""
        return self._layer_time

    @layer_time.setter
    def layer_time(self, value: float | None = None):
        self._layer_time = float(value) if value is not None else None

    @property
    def pause_duration(self) -> int | None:
        """Total pause time since the job started"""
        return self._pause_duration

    @pause_duration.setter
    def pause_duration(self, value: int | None = None):
        self._pause_duration = int(value) if value is not None else None

    @property
    def raw_extrusion(self) -> float | None:
        """Total extrusion amount without extrusion factors applied (in mm)"""
        return self._raw_extrusion

    @raw_extrusion.setter
    def raw_extrusion(self, value: float | None = None):
        self._raw_extrusion = float(value) if value is not None else None

    @property
    def times_left(self) -> TimesLeft:
        """Estimated times left"""
        return self._times_left

    @property
    def warm_up_duration(self) -> int | None:
        """Time needed to heat up the heaters (in s or null)"""
        return self._warm_up_duration

    @warm_up_duration.setter
    def warm_up_duration(self, value: int | None = None):
        self._warm_up_duration = int(value) if value is not None else None
