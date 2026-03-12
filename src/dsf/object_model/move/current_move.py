from typing import Union

from ..model_object import ModelObject


class CurrentMove(ModelObject):
    """Information about the current move"""
    def __init__(self):
        super().__init__()
        # Acceleration of the current move (in mm/s^2)
        self._acceleration: float = 0
        # Deceleration of the current move (in mm/s^2)
        self._deceleration: float = 0
        # Total distance of the current move (in mm)
        self._distance: float = 0
        # Duration of the current move (in s)
        self._duration: float = 0
        # Current extrusion rate (in mm/s)
        self._extrusion_rate: float = 0
        # Laser PWM of the current move (0..1) or null if not applicable
        self._laser_pwm: Union[float, None] = None
        # Requested speed of the current move (in mm/s)
        self._requested_speed: float = 0
        # Top speed of the current move (in mm/s)
        self._top_speed: float = 0

    @property
    def acceleration(self) -> float:
        """Acceleration of the current move (in mm/s^2)"""
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value: float | int | str):
        self._acceleration = float(value)

    @property
    def deceleration(self) -> float:
        """Deceleration of the current move (in mm/s^2)"""
        return self._deceleration

    @deceleration.setter
    def deceleration(self, value: float | int | str):
        self._deceleration = float(value)

    @property
    def distance(self) -> float:
        """Total distance of the current move (in mm)"""
        return self._distance

    @distance.setter
    def distance(self, value: float):
        self._distance = float(value)

    @property
    def duration(self) -> float:
        """Duration of the current move (in s)"""
        return self._duration

    @duration.setter
    def duration(self, value: float):
        self._duration = float(value)

    @property
    def extrusion_rate(self) -> float:
        """Current extrusion rate (in mm/s)"""
        return self._extrusion_rate

    @extrusion_rate.setter
    def extrusion_rate(self, value: float | int | str):
        self._extrusion_rate = float(value)

    @property
    def laser_pwm(self) -> Union[float, None]:
        """Laser PWM of the current move (0..1) or null if not applicable"""
        return self._laser_pwm

    @laser_pwm.setter
    def laser_pwm(self, value: float | int | str | None):
        self._laser_pwm = float(value) if value is not None else None

    @property
    def requested_speed(self) -> float:
        """Requested speed of the current move (in mm/s)"""
        return self._requested_speed

    @requested_speed.setter
    def requested_speed(self, value: float | int | str):
        self._requested_speed = float(value)

    @property
    def top_speed(self) -> float:
        """Top speed of the current move (in mm/s)"""
        return self._top_speed

    @top_speed.setter
    def top_speed(self, value: float | int | str):
        self._top_speed = float(value)
