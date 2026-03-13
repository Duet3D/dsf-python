from ..model_object import ModelObject
from ..utils import model_prop


class BoardClosedLoop(ModelObject):
    """This represents information about closed-loop tuning"""

    # Number of collected data points in the last run or 0 if it failed
    points = model_prop("points", int)

    # Number of completed sampling runs
    runs = model_prop("runs", int)

    def __init__(self):
        super(BoardClosedLoop, self).__init__()
