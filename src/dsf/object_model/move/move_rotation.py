from typing import List

from ..model_object import ModelObject


class MoveRotation(ModelObject):
    """Information about centre rotation as defined by G68"""

    def __init__(self) -> None:
        super().__init__()
        # Angle of the centre rotatation (in deg)
        self._angle: float = 0
        # XY coordinates of the centre rotation
        self._centre: List[float] = [0.0, 0.0]

    @property
    def angle(self) -> float:
        """Angle of the centre rotatation (in deg)"""
        return self._angle

    @angle.setter
    def angle(self, value: float | int | str):
        self._angle = float(value)

    @property
    def centre(self) -> List[float]:
        """XY coordinates of the centre rotation"""
        return self._centre
