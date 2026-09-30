from ..model_object import ModelObject
from ..utils import model_prop


class Accelerometer(ModelObject):
    """
    This represents an accelerometer
    The index of an accelerometer in the sensors.accelerometers list is the P number used by M955 and M956
    """

    # Orientation of the accelerometer
    # See the following page for a list of orientations:
    # https://docs.duet3d.com/en/Duet3D_hardware/Accessories/Duet3D_Accelerometer#orientation
    orientation = model_prop("orientation", int, 20)

    # Number of collected data points in the last run or 0 if it failed
    points = model_prop("points", int)

    # Port name(s) the accelerometer is connected to as passed to M955 C,
    # including the CAN address prefix on expansion boards
    port = model_prop("port", str, "")

    # Resolution the accelerometer is programmed for (in bits) or 0 if unknown
    resolution = model_prop("resolution", int)

    # Number of completed sampling runs
    runs = model_prop("runs", int)

    # Rate the accelerometer is programmed for (in Hz) or 0 if unknown
    # This is the rate the accelerometer settled on, which may be lower than the one M955 asked for.
    # Once it has completed a run, the rate measured during that run is reported instead
    sampling_rate = model_prop("sampling_rate", int)

    def __init__(self):
        super(Accelerometer, self).__init__()
