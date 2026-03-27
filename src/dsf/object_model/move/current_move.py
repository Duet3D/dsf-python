from ..model_object import ModelObject
from ..utils import model_prop, nullable_model_prop


class CurrentMove(ModelObject):
    """Information about the current move"""

    # Acceleration of the current move (in mm/s^2)
    acceleration = model_prop("acceleration", float, 0.0)

    # Deceleration of the current move (in mm/s^2)
    deceleration = model_prop("deceleration", float, 0.0)

    # Total distance of the current move (in mm)
    distance = model_prop("distance", float, 0.0)

    # Duration of the current move (in s)
    duration = model_prop("duration", float, 0.0)

    # Current extrusion rate (in mm/s)
    extrusion_rate = model_prop("extrusion_rate", float, 0.0)

    # Laser PWM of the current move (0..1) or null if not applicable
    laser_pwm = nullable_model_prop("laser_pwm", float)

    # Requested speed of the current move (in mm/s)
    requested_speed = model_prop("requested_speed", float, 0.0)

    # Top speed of the current move (in mm/s)
    top_speed = model_prop("top_speed", float, 0.0)

    def __init__(self):
        super().__init__()
        self._acceleration = 0.0
        self._deceleration = 0.0
        self._distance = 0.0
        self._duration = 0.0
        self._extrusion_rate = 0.0
        self._laser_pwm = None
        self._requested_speed = 0.0
        self._top_speed = 0.0
