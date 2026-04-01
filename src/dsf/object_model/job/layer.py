from typing import Optional

from ..model_object import ModelObject
from ..model_collection import ModelCollection
from ..utils import model_prop


class Layer(ModelObject):
    """Information about a layer from a file being printed"""

    # Duration of the layer (in s)
    duration = model_prop("duration", float, 0.0)

    # Amount of total filament extruded during this layer (in mm)
    filament_usage = model_prop("filament_usage", float, 0.0)

    # Fraction of the file printed during this layer (0..1)
    fraction_printed = model_prop("fraction_printed", float, 0.0)

    # Height of the layer (in mm or 0 if unknown)
    height = model_prop("height", float, 0.0)

    # Last heater temperatures during this layer (in C or null if unknown)
    temperatures = model_prop("temperatures", ModelCollection[Optional[float]], ModelCollection(Optional[float]))

    def __init__(self):
        super().__init__()
