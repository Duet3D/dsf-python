from ..model_object import ModelObject
from ..utils import nullable_model_prop, model_prop


class ExtruderPressureAdvance(ModelObject):
    """Information about an extruder drive"""

    # Delay coefficient (in ms), or null if pressure advance is in simple mode (k0 = 0) - RRF reports infinity here as null
    d = nullable_model_prop("d", float)

    # K0 coefficient
    k0 = model_prop("k0", float, 0.0)

    # K1 coeffient
    k1 = model_prop("k1", float, 0.0)
    
    def __init__(self):
        super().__init__()
