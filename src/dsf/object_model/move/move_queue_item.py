from ..model_object import ModelObject


class MoveQueueItem(ModelObject):
    """Information about a DDA ring"""
    def __init__(self):
        super().__init__()
        # The minimum idle time before we should start a move (in s)
        self._grace_period = 0
        # Maximum number of moves that can be accomodated in the DDA ring
        self._length = 0

    @property
    def grace_period(self) -> float:
        """The minimum idle time before we should start a move (in s)"""
        return self._grace_period

    @grace_period.setter
    def grace_period(self, value):
        self._grace_period = float(value) if value is not None else 0

    @property
    def length(self) -> int:
        """Maximum number of moves that can be accomodated in the DDA ring"""
        return self._length

    @length.setter
    def length(self, value):
        self._length = int(value) if value is not None else 0
