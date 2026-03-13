from ..model_object import ModelObject
from ..utils import model_prop


class Accelerometer(ModelObject):
    """This represents an accelerometer"""
    # Orientation of the accelerometer
    # See https://docs.duet3d.com/en/Duet3D_hardware/Accessories/Duet3D_Accelerometer#orientation for a list of orientations
    orientation = model_prop("orientation", int, 20)

    # Number of collected data points in the last run or 0 if it failed
    points = model_prop("points", int)

    # Number of completed sampling runs
    runs = model_prop("runs", int)
    
    def __init__(self):
        super(Accelerometer, self).__init__()

