from ..model_object import ModelObject
from ..utils import model_prop


class MoveQueueItem(ModelObject):
    """Information about a DDA ring"""

    # The minimum idle time before we should start a move (in s)
    grace_period = model_prop("grace_period", float, 0)

    # Maximum number of moves that can be accomodated in the DDA ring
    length = model_prop("length", int, 0)

    def __init__(self):
        super().__init__()
