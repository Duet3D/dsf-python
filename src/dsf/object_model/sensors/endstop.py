from .endstop_type import EndstopType
from ..model_object import ModelObject
from ..utils import nullable_model_prop, model_prop


class Endstop(ModelObject):
    """Information about an endstop"""

    # Whether this endstop is at the high end of the axis
    high_end = model_prop("high_end", bool)

    # Number of the referenced probe if type is ZProbeAsEndstop, else None
    probe = nullable_model_prop("probe", int)

    # Whether the endstop is hit
    triggered = model_prop("triggered", bool)

    # Type of the endstop
    type = model_prop("type", EndstopType, EndstopType.Unknown)

    def __init__(self):
        super(Endstop, self).__init__()
