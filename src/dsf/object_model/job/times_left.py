from typing import Union

from ..model_object import ModelObject
from ..utils import nullable_model_prop


class TimesLeft(ModelObject):
    """Estimations about the times left"""

    # Time left based on filament consumption (in s or null)
    filament = nullable_model_prop("filament", int)

    # Time left based on file progress (in s or null)
    file = nullable_model_prop("file", int)

    # Time left based on the slicer reports (see M73, in s or null)
    slicer = nullable_model_prop("slicer", int)

    # Time left before the next colour change is expected (see M73 C, in s or null)
    to_pause = nullable_model_prop("to_pause", int)

    def __init__(self):
        super().__init__()
