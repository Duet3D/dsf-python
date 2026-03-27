from ..model_object import ModelObject
from ..utils import model_prop, nullable_model_prop


class CPU(ModelObject):
    """Information about the SBC's CPU"""

    avg_load = nullable_model_prop("avg_load", float)
    hardware = nullable_model_prop("hardware", str)
    num_cores = model_prop("num_cores", int, 1)
    temperature = nullable_model_prop("temperature", float)

    def __init__(self):
        super().__init__()

