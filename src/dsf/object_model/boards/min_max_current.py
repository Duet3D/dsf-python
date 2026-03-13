from ..model_object import ModelObject
from ..utils import model_prop

class MinMaxCurrent(ModelObject):
    """Provides minimum, maximum and current values"""

    # Current value
    current = model_prop("current", float)
    
    # Minimum value
    min = model_prop("min", float)

    # Maximum value
    max = model_prop("max", float)

    def __init__(self):
        super(MinMaxCurrent, self).__init__()
    