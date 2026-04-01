from typing import Optional

from .heater import Heater
from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import model_prop


class Heat(ModelObject):
    """Information about the heat subsystem"""

    # List of configured bed heaters (indices)
    # deprecated, use bed_heater_mapping instead
    bed_heaters = model_prop("bed_heaters", ModelCollection[int], ModelCollection(int))

    # List of configured bed heaters (indices), grouped by bed (first dimension)
    bed_heater_mapping = model_prop("bed_heater_mapping", ModelCollection[list[int]], ModelCollection(list[int]))

    # List of configured chamber heaters (indices)
    # deprecated, use chamber_heater_mapping instead
    chamber_heaters = model_prop("chamber_heaters", ModelCollection[int], ModelCollection(int))

    # List of configured chamber heaters (indices), grouped by chamber (first dimension)
    chamber_heater_mapping = model_prop("chamber_heater_mapping", ModelCollection[list[int]], ModelCollection(list[int]))

    # Minimum required temperature for extrusion moves (in C)
    cold_extrude_temperature = model_prop("cold_extrude_temperature", float, 160)

    # Minimum required temperature for retraction moves (in C)
    cold_retract_temperature = model_prop("cold_retract_temperature", float, 90)

    # List of configured Heaters
    heaters = model_prop("heaters", ModelCollection[Optional[Heater]], ModelCollection(Optional[Heater]))

    def __init__(self):
        super().__init__()
