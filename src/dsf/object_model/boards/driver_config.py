from .driver_mode import DriverMode
from ..model_object import ModelObject
from ..utils import nullable_model_prop, model_prop


class DriverConfig(ModelObject):
    """Configured (M569) settings of a driver"""

    # Configured direction of the driver (false = reverse, true = forward)
    direction = model_prop('direction', bool, True)

    # Configured driver mode (only available for smart drivers)
    mode = nullable_model_prop('mode', DriverMode, lambda: None)

    def __init__(self):
        super(DriverConfig, self).__init__()
