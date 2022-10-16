from typing import Union

from ..model_object import ModelObject


class CurrentMove(ModelObject):
    """Information about the current move"""
    def __init__(self):
        super().__init__()
        # Acceleration of the current move (in mm/s^2)
        self._acceleration = 0
        # Deceleration of the current move (in mm/s^2)
        self._deceleration = 0
        # Laser PWM of the current move (0..1) or null if not applicable
        self._laser_pwm = None
        # Requested speed of the current move (in mm/s)
        self._requested_speed = 0
        # Top speed of the current move (in mm/s)
        self._top_speed = 0

    @property
    def acceleration(self) -> float:
        """Acceleration of the current move (in mm/s^2)"""
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = float(value) if value is not None else 0

    @property
    def deceleration(self) -> float:
        """Deceleration of the current move (in mm/s^2)"""
        return self._deceleration

    @deceleration.setter
    def deceleration(self, value):
        self._deceleration = float(value)

    @property
    def laser_pwm(self) -> Union[float, None]:
        """Laser PWM of the current move (0..1) or null if not applicable"""
        return self._laser_pwm

    @laser_pwm.setter
    def laser_pwm(self, value):
        self._laser_pwm = float(value) if value is not None else None

    @property
    def requested_speed(self) -> float:
        """Requested speed of the current move (in mm/s)"""
        return self._requested_speed

    @requested_speed.setter
    def requested_speed(self, value):
        self._requested_speed = float(value)

    @property
    def top_speed(self) -> float:
        """Top speed of the current move (in mm/s)"""
        return self._top_speed

    @top_speed.setter
    def top_speed(self, value):
        self._top_speed = float(value)
