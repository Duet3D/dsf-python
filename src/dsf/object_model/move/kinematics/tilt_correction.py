from typing import List

from ...model_object import ModelObject
from ...model_collection import ModelCollection
from ...utils import model_prop


class TiltCorrection(ModelObject):
    """Tilt correction parameters for Z leadscrew compensation"""

    # Correction factor
    correction_factor = model_prop("correction_factor", float, 0.0)

    # Last corrections (in mm)
    last_corrections = model_prop("last_corrections", ModelCollection[float], ModelCollection(float, []))

    # Maximum Z correction (in mm)
    max_correction = model_prop("max_correction", float, 0.0)

    # Pitch of the Z leadscrews (in mm)
    screw_pitch = model_prop("screw_pitch", float, 0.0)

    # X positions of the leadscrews (in mm)
    screw_x = model_prop("screw_x", ModelCollection[float], ModelCollection(float, []))

    # Y positions of the leadscrews (in mm)
    screw_y = model_prop("screw_y", ModelCollection[float], ModelCollection(float, []))

    def __init__(self):
        super().__init__()
