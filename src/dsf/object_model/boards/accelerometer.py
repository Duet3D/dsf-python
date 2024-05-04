from ..model_object import ModelObject


class Accelerometer(ModelObject):
    """This represents an accelerometer"""
    def __init__(self):
        super(Accelerometer, self).__init__()
        # Orientation of the accelerometer
        # See https://docs.duet3d.com/en/Duet3D_hardware/Accessories/Duet3D_Accelerometer#orientation for a list of orientations
        self._orientation = 20
        # Number of collected data points in the last run or 0 if it failed
        self._points = 0
        # Number of completed sampling runs
        self._runs = 0

    @property
    def orientation(self) -> int:
        """Orientation of the accelerometer
        See https://docs.duet3d.com/en/Duet3D_hardware/Accessories/Duet3D_Accelerometer#orientation for a list of orientations"""
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = int(value)

    @property
    def points(self) -> int:
        """Number of collected data points in the last run or 0 if it failed"""
        return self._points

    @points.setter
    def points(self, value: int):
        self._points = int(value)

    @property
    def runs(self) -> int:
        """Number of completed sampling runs"""
        return self._runs

    @runs.setter
    def runs(self, value: int):
        self._runs = int(value)
