from typing import List, Union

from .build import Build
from .gcode_fileinfo import GCodeFileInfo
from .layer import Layer
from .times_left import TimesLeft
from ..model_object import ModelObject


class Job(ModelObject):
    """Information about the current job"""
    def __init__(self):
        super().__init__()
        # Information about the current build or null if not available
        self._build = Build()
        # Total active duration of the current job file (in s or null)
        self._duration = None
        # Information about the file being processed
        self._file = GCodeFileInfo()
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
        self._layers = []
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
    def build(self) -> Build:
        """Information about the current build or null if not available"""
        return self._build

    @build.setter
    def build(self, value):
        if value is None or isinstance(value, Build):
            self._build = value
        elif isinstance(value, dict):  # Update from JSON
            self._build = Build.from_json(value)
        else:
            raise TypeError(f"{__name__}.build must be None or of type Build. Got {type(value)}: {value}")

    @property
    def duration(self) -> Union[int, None]:
        """Total active duration of the current job file (in s or null)"""
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = int(value) if value is not None else None

    @property
    def file(self) -> GCodeFileInfo:
        """Information about the file being processed"""
        return self._file

    @property
    def file_position(self) -> Union[int, None]:
        """Current position in the file being processed (in bytes or null)"""
        return self._file_position

    @file_position.setter
    def file_position(self, value):
        self._file_position = int(value) if value is not None else None

    @property
    def last_duration(self) -> Union[int, None]:
        """Total duration of the last job (in s or null)"""
        return self._last_duration

    @last_duration.setter
    def last_duration(self, value):
        self._last_duration = int(value) if value is not None else None

    @property
    def last_file_aborted(self) -> bool:
        """Indicates if the last file was aborted (unexpected cancellation)"""
        return self._last_file_aborted

    @last_file_aborted.setter
    def last_file_aborted(self, value):
        self._last_file_aborted = bool(value)

    @property
    def last_file_cancelled(self) -> bool:
        """Indicates if the last file was cancelled (user cancelled)"""
        return self._last_file_cancelled

    @last_file_cancelled.setter
    def last_file_cancelled(self, value):
        self._last_file_cancelled = bool(value)

    @property
    def last_file_name(self) -> Union[str, None]:
        """Name of the last file processed or null if none"""
        return self._last_file_name

    @last_file_name.setter
    def last_file_name(self, value):
        self._last_file_name = str(value) if value is not None else None

    @property
    def last_file_simulated(self) -> bool:
        """Indicates if the last file processed was simulated
        This is not set if the file was aborted or cancelled"""
        return self._last_file_simulated

    @last_file_simulated.setter
    def last_file_simulated(self, value):
        self._last_file_simulated = bool(value)

    @property
    def layer(self) -> Union[int, None]:
        """Number of the current layer or null not available"""
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = int(value) if value is not None else None

    @property
    def layers(self) -> List[Layer]:
        """Information about the past layers
        In previous API versions this was a ModelGrowingCollection{T} but it has been changed to ModelCollection{T} to
        allow past layers to be modified again when needed.
        Note that previous plugins subscribing to this property will not receive any more updates about this property
        to avoid memory leaks.
        See also Layer"""
        return self._layers

    @property
    def layer_time(self) -> Union[float, None]:
        """Time elapsed since the last layer change (in s or null)"""
        return self.layer_time

    @layer_time.setter
    def layer_time(self, value):
        self._layer_time = float(value) if value is not None else None

    @property
    def pause_duration(self) -> Union[int, None]:
        """Total pause time since the job started"""
        return self.pause_duration

    @pause_duration.setter
    def pause_duration(self, value):
        self._pause_duration = int(value) if value is not None else None

    @property
    def raw_extrusion(self) -> Union[float, None]:
        """Total extrusion amount without extrusion factors applied (in mm)"""
        return self._raw_extrusion

    @raw_extrusion.setter
    def raw_extrusion(self, value):
        self._raw_extrusion = float(value) if value is not None else None

    @property
    def times_left(self) -> TimesLeft:
        """Estimated times left"""
        return self._times_left

    @property
    def warm_up_duration(self) -> Union[int, None]:
        """Time needed to heat up the heaters (in s or null)"""
        return self._warm_up_duration

    @warm_up_duration.setter
    def warm_up_duration(self, value):
        self._warm_up_duration = int(value) if value is not None else None

    def _update_from_json(self, **kwargs) -> 'Job':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(Job, self)._update_from_json(**kwargs)
        file = kwargs.get('file')
        self._file = GCodeFileInfo.from_json(file) if file is not None else None
        self._layers = [Layer.from_json(layer_) for layer_ in kwargs.get('layers', [])]
        times_left = kwargs.get('timesLeft')
        self._times_left = TimesLeft.from_json(times_left) if times_left is not None else None
        return self
