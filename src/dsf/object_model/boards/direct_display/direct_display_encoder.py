from ...model_object import ModelObject
from ...utils import model_prop


class DirectDisplayEncoder(ModelObject):
    """Class providing information about a connected display encoder"""

    # Number of pulses per click of the rotary encoder
    pulses_per_click = model_prop("pulses_per_click", int, 1)

    def __init__(self):
        super().__init__()
