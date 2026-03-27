from datetime import datetime
from typing import List, Union

from .thumbnail_info import ThumbnailInfo
from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..model_dictionary import ModelDictionary
from ..utils import model_prop, nullable_model_prop


class GCodeFileInfo(ModelObject):
    """Holds information about a parsed G-code file"""

    # User-defined key-value pairs
    custom_info = model_prop("custom_info", ModelDictionary, ModelDictionary(False))

    # Filament consumption per extruder drive (in mm)
    filament = model_prop("filament", ModelCollection[float], ModelCollection(float))

    # The filename of the G-code file
    file_name = nullable_model_prop("file_name", str)

    # Name of the application that generated this file
    generated_by = nullable_model_prop("generated_by", str)

    # Build height of the G-code job or 0 if not found (in mm)
    height = model_prop("height", float, 0.0)

    # Value indicating when the file was last modified or null if unknown
    last_modified = nullable_model_prop("last_modified", datetime, lambda: None)

    # Height of each other layer or 0 if not found (in mm)
    layer_height = model_prop("layer_height", float, 0.0)

    # Number of total layers or 0 if unknown
    num_layers = model_prop("num_layers", int, 0)

    # Estimated print time (in s)
    print_time = nullable_model_prop("print_time", int)

    # Estimated print time from G-code simulation (in s)
    simulated_time = nullable_model_prop("simulated_time", int)

    # Size of the file
    size = nullable_model_prop("size", int)

    # Collection of thumbnails parsed from Gcode
    thumbnails = model_prop("thumbnails", ModelCollection[ThumbnailInfo], ModelCollection(ThumbnailInfo))

    def __init__(self):
        super().__init__()
