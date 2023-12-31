from .driver_closed_loop import DriverClosedLoop
from ..model_object import ModelObject
from ..utils import wrap_model_property


class Driver(ModelObject):
    """Information about a driver"""

    # Closed-loop settings (if applicable)
    closed_loop = wrap_model_property('closed_loop', DriverClosedLoop)

    def __init__(self):
        super(Driver, self).__init__()
        # Closed-loop settings (if applicable)
        self._closed_loop = None
        # Driver status register value
        self._status = 0

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value):
        """Driver status register value
        The lowest 8 bits of these have the same bit positions as in the TMC2209 DRV_STATUS register.
        The TMC5160 DRV_STATUS is different so the bits are translated to this. Similarly for TMC2660.
        Only the lowest 16 bits are passed in driver event messages"""
        self._status = int(value)
