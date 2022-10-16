from ..model_object import ModelObject


class Skew(ModelObject):
    """Class holding details about orthogonoal axis compensation parameters"""

    def __init__(self):
        super().__init__()
        # Indicates if the TanXY value is used to compensate X when Y moves (else Y when X moves)
        self._compensate_XY = True
        # Tangent of the skew angle for the XY or YX axes
        self._tan_XY = 0
        # Tangent of the skew angle for the XZ axes
        self._tan_XZ = 0
        # Tangent of the skew angle for the YZ axes
        self._tan_YZ = 0

    @property
    def compensate_XY(self) -> bool:
        """Indicates if the TanXY value is used to compensate X when Y moves (else Y when X moves)"""
        return self._compensate_XY

    @compensate_XY.setter
    def compensate_XY(self, value):
        self._compensate_XY = bool(value)

    @property
    def tan_XY(self) -> float:
        """Tangent of the skew angle for the XY or YX axes"""
        return self._tan_XY

    @tan_XY.setter
    def tan_XY(self, value):
        self._tan_XY = float(value) if value is not None else 0

    @property
    def tan_XZ(self) -> float:
        """Tangent of the skew angle for the XZ axes"""
        return self._tan_XZ

    @tan_XZ.setter
    def tan_XZ(self, value):
        self._tan_XZ = float(value) if value is not None else 0

    @property
    def tan_YZ(self) -> float:
        """Tangent of the skew angle for the YZ axes"""
        return self._tan_YZ

    @tan_YZ.setter
    def tan_YZ(self, value):
        self._tan_YZ = float(value) if value is not None else 0
