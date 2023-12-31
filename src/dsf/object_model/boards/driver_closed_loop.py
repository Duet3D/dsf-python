from ..model_object import ModelObject


class ClosedLoopCurrentFraction(ModelObject):
    """Information about the current fraction of the closed-loop configuration"""
    def __init__(self):
        super(ClosedLoopCurrentFraction, self).__init__()
        # Average fraction
        self._avg = 0
        # Maximum fraction
        self._max = 0

    @property
    def avg(self) -> float:
        """Average fraction"""
        return self._avg

    @avg.setter
    def avg(self, value):
        self._avg = float(value)

    @property
    def max(self) -> float:
        """Maximum fraction"""
        return self._max

    @max.setter
    def max(self, value):
        self._max = float(value)


class ClosedLoopPositionError(ModelObject):
    """Information about the current fraction of the closed-loop configuration"""
    def __init__(self):
        super(ClosedLoopPositionError, self).__init__()
        # Maximum position error
        self._max = 0
        # RMS of the position error
        self._rms = 0

    @property
    def max(self) -> float:
        """Maximum position error"""
        return self._max

    @max.setter
    def max(self, value):
        self._max = float(value)

    @property
    def rms(self) -> float:
        """RMS of the position error"""
        return self._rms

    @rms.setter
    def rms(self, value):
        self._rms = float(value)


class DriverClosedLoop(ModelObject):
    """This represents information about closed-loop tuning"""
    def __init__(self):
        super(DriverClosedLoop, self).__init__()
        # Current fraction
        self._current_fraction = ClosedLoopCurrentFraction()
        # Position
        self._position_error = ClosedLoopPositionError()
    
    @property
    def current_fraction(self):
        """Current fraction"""
        return self._current_fraction
    
    @property
    def position_error(self):
        """Position error"""
        return self._position_error
