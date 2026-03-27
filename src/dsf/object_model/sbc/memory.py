from ..model_object import ModelObject
from ..utils import nullable_model_prop


class Memory(ModelObject):
    """Information about the SBC's memory (RAM)"""

    available = nullable_model_prop("available", int)
    total = nullable_model_prop("total", int)

    def __init__(self):
        super().__init__()
