from ..model_object import ModelObject


class MinMaxCurrent(ModelObject):
    """Provides minimum, maximum and current values"""

    def __init__(self):
        super(MinMaxCurrent, self).__init__()
        # Current value (mA)
        self._current = 0
        # Minimum value (mA)
        self._min = 0
        # Maximum value (mA)
        self._max = 0

    @property
    def current(self) -> float:
        """Current value (mA)"""
        return self._current

    @current.setter
    def current(self, value: float):
        self._current = float(value) if value is not None else 0

    @property
    def min(self) -> float:
        """Minimum value (mA)"""
        return self._min

    @min.setter
    def min(self, value: float):
        self._min = float(value) if value is not None else 0

    @property
    def max(self) -> float:
        """Maximum value (mA)"""
        return self._max

    @max.setter
    def max(self, value: float):
        self._max = float(value) if value is not None else 0
