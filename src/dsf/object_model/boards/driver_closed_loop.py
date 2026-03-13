from ..model_object import ModelObject
from ..utils import model_prop


class ClosedLoopCurrentFraction(ModelObject):
    """Information about the current fraction of the closed-loop configuration"""

    # Average fraction
    avg = model_prop("avg", float)

    # Maximum fraction
    max = model_prop("max", float)

    def __init__(self):
        super(ClosedLoopCurrentFraction, self).__init__()


class ClosedLoopPositionError(ModelObject):
    """Information about the current fraction of the closed-loop configuration"""

    # Maximum position error
    max = model_prop("max", float)

    # RMS of the position error
    rms = model_prop("rms", float)

    def __init__(self):
        super(ClosedLoopPositionError, self).__init__()


class DriverClosedLoop(ModelObject):
    """This represents information about closed-loop tuning"""
    
    # Current fraction of the configured motor current used
    current_fraction = model_prop("current_fraction", ClosedLoopCurrentFraction)

    # Position error in full steps of the motor
    position_error = model_prop("position_error", ClosedLoopPositionError)

    def __init__(self):
        super(DriverClosedLoop, self).__init__()
