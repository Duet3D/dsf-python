from ..model_object import ModelObject
from ..utils import model_prop, nullable_model_prop


class Upgrade(ModelObject):
    """Details about a software upgrade in progress"""

    # Description of the current upgrade step
    message = model_prop("message", str, "")

    # Progress of the current upgrade step (0..1) or None if indeterminate
    progress = nullable_model_prop("progress", float)

    def __init__(self):
        super().__init__()
