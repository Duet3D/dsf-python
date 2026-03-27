from typing import List

from .build_object import BuildObject
from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import model_prop


class Build(ModelObject):
    """Information about the current build"""

    # Index of the current object being printed or -1 if unknown
    current_object = model_prop("current_object", int, -1)

    # Whether M486 names are being used
    m486_names = model_prop("m486_names", bool, False)

    # Whether M486 numbers are being used
    m486_numbers = model_prop("m486_numbers", bool, False)

    # List of detected build objects
    objects = model_prop("objects", ModelCollection[BuildObject], ModelCollection(BuildObject))

    def __init__(self):
        super().__init__()
