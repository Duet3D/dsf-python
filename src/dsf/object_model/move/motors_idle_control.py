from ..model_object import ModelObject
from ..utils import model_prop


class MotorsIdleControl(ModelObject):
    """Idle factor parameters for automatic motor current reduction"""

    # Motor current reduction factor (0..1)
    factor = model_prop("factor", float, 0.3)

    # Idle timeout after which the stepper motor currents are reduced (in s)
    timeout = model_prop("timeout", float, 30)

    def __init__(self):
        super().__init__()
