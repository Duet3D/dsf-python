from .driver_closed_loop import DriverClosedLoop
from ..model_object import ModelObject
from ..utils import nullable_model_prop, model_prop


class Driver(ModelObject):
    """Information about a driver"""

    # Closed-loop settings (if applicable)
    closed_loop = nullable_model_prop('closed_loop', DriverClosedLoop)

    # Driver status register value
    status = model_prop("status", int)

    def __init__(self):
        super(Driver, self).__init__()
