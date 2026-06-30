from .driver_closed_loop import DriverClosedLoop
from .driver_config import DriverConfig
from ..model_object import ModelObject
from ..utils import nullable_model_prop, model_prop


class Driver(ModelObject):
    """Information about a driver"""

    # Closed-loop settings (if applicable)
    closed_loop = nullable_model_prop('closed_loop', DriverClosedLoop)

    # Configured (M569) settings of this driver
    config = model_prop('config', DriverConfig)

    # Driver status register value
    status = model_prop("status", int)

    def __init__(self):
        super(Driver, self).__init__()
