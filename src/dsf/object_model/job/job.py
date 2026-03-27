from typing import List, Union

from .build import Build
from .gcode_fileinfo import GCodeFileInfo
from .layer import Layer
from .times_left import TimesLeft
from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import nullable_model_prop, model_prop


class Job(ModelObject):
    """Information about the current job"""

    # Information about the current build or None if not available
    build = nullable_model_prop('build', Build)
    # Total active duration of the current job file (in s or None)
    duration = nullable_model_prop('duration', int)
    # Information about the file being processed
    file = model_prop('file', GCodeFileInfo)
    # Current position in the file being processed (in bytes or None)
    file_position = nullable_model_prop('file_position', int)
    # Total duration of the last job (in s or None)
    last_duration = nullable_model_prop('last_duration', int)
    # Name of the last file processed or None
    last_file_name = nullable_model_prop('last_file_name', str)
    # Indicates if the last file was aborted (unexpected cancellation)
    last_file_aborted = model_prop('last_file_aborted', bool, False)
    # Indicates if the last file was cancelled (user cancelled)
    last_file_cancelled = model_prop('last_file_cancelled', bool, False)
    # Indicates if the last file processed was simulated
    last_file_simulated = model_prop('last_file_simulated', bool, False)
    # Warm-up duration of the last print or None if not available (in s)
    last_warm_up_duration = nullable_model_prop('last_warm_up_duration', int)
    # Number of the current layer or None if not available
    layer = nullable_model_prop('layer', int)
    # Information about the past layers
    layers = model_prop('layers', ModelCollection[Layer], ModelCollection(Layer))
    # Time elapsed since the last layer change (in s or None)
    layer_time = nullable_model_prop('layer_time', float)
    # Total pause time since the job started
    pause_duration = nullable_model_prop('pause_duration', int)
    # Total extrusion amount without extrusion factors applied (in mm)
    raw_extrusion = nullable_model_prop('raw_extrusion', float)
    # Estimated times left
    times_left = model_prop('times_left', TimesLeft)
    # Time needed to heat up the heaters (in s or None)
    warm_up_duration = nullable_model_prop('warm_up_duration', int)

    def __init__(self):
        super().__init__()
