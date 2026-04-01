from typing import Optional

from ..model_object import ModelObject
from ..model_collection import ModelCollection
from ..utils import model_prop, nullable_model_prop


class BuildObject(ModelObject):
    """Information about a detected build object"""

    # Indicates if this build object is cancelled
    canceled = model_prop("canceled", bool, False)

    # Name of the build object (if any)
    name = nullable_model_prop("name", str)

    # X coordinates of the build object (in mm or null if not found)
    x = model_prop("x", ModelCollection[Optional[float]], ModelCollection(Optional[float]))

    # Y coordinates of the build object (in mm or null if not found)
    y = model_prop("y", ModelCollection[Optional[float]], ModelCollection(Optional[float]))

    def __init__(self):
        super().__init__()
