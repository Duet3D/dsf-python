from __future__ import annotations

from .probe_type import ProbeType
from ..model_object import ModelObject


class Probe(ModelObject):
    """Information about a configured probe"""

    def __init__(self):
        super(Probe, self).__init__()
        self._calibration_temperature = 0
        self._deployed_by_user = False
        self._disables_heaters = False
        self._dive_height = 0
        self._last_stop_height = 0
        self._max_probe_count = 1
        self._offsets = [0, 0]
        self._recovery_time = 0
        self._speeds = [2, 2]
        self._temperature_coefficients = [0, 0]
        self._threshold = 500
        self._tolerance = 0.03
        self._travel_speed = 6000
        self._trigger_height = 0.7
        self._type = ProbeType.NoProbe
        self._value = []

    @property
    def calibration_temperature(self) -> float:
        """Calibration temperature (in C)"""
        return self._calibration_temperature
    
    @calibration_temperature.setter
    def calibration_temperature(self, value: float):
        self._calibration_temperature = float(value)
        
    @property
    def deployed_by_user(self) -> bool:
        """Indicates if the user has deployed the probe"""
        return self._deployed_by_user
    
    @deployed_by_user.setter
    def deployed_by_user(self, value: bool):
        self._deployed_by_user = bool(value)
        
    @property
    def disables_heaters(self) -> bool:
        """Whether probing disables the heater(s)"""
        return self._disables_heaters
    
    @disables_heaters.setter
    def disables_heaters(self, value: bool):
        self._disables_heaters = bool(value)
        
    @property
    def dive_height(self) -> float:
        """Dive height (in mm)"""
        return self._dive_height
    
    @dive_height.setter
    def dive_height(self, value: float):
        self._dive_height = float(value)
        
    @property
    def last_stop_height(self) -> float:
        """Height of the probe where it stopped last time (in mm)"""
        return self._last_stop_height
    
    @last_stop_height.setter
    def last_stop_height(self, value: float):
        self._last_stop_height = float(value)
        
    @property
    def max_probe_count(self) -> int:
        """Maximum number of times to probe after a bad reading was determined"""
        return self._max_probe_count
    
    @max_probe_count.setter
    def max_probe_count(self, value: int):
        self._max_probe_count = int(value)
        
    @property
    def offsets(self) -> list[float]:
        """X+Y offsets (in mm)"""
        return self._offsets
    
    @property
    def recovery_time(self) -> float:
        """Recovery time (in s)"""
        return self._recovery_time
    
    @recovery_time.setter
    def recovery_time(self, value: float):
        self._recovery_time = float(value)
        
    @property
    def speed(self) -> float:
        """Probe speed (in mm/s)
        Obsolete: Use Speeds[0] instead"""
        return self._speeds[0]
    
    @speed.setter
    def speed(self, value: float):
        self._speeds[0] = float(value)
        
    @property
    def speeds(self) -> list[float]:
        """Fast and slow probing speeds (in mm/s)"""
        return self._speeds
    
    @speeds.setter
    def speeds(self, values: list[float]):
        self._speeds = [float(value) for value in values]
        
    @property
    def temperature_coefficient(self) -> float:
        """First temperature coefficient
        Obsolete: Use TemperatureCoefficients instead"""
        return self._temperature_coefficients[0]
    
    @temperature_coefficient.setter
    def temperature_coefficient(self, value: float):
        self._temperature_coefficients[0] = float(value)
        
    @property
    def temperature_coefficients(self) -> list[float]:
        """List of temperature coefficients"""
        return self._temperature_coefficients
        
    @property
    def threshold(self) -> int:
        """Configured trigger threshold (0..1023)"""
        return self._threshold
    
    @threshold.setter
    def threshold(self, value: int):
        self._threshold = int(value)
        
    @property
    def tolerance(self) -> float:
        """Allowed tolerance deviation between two measures (in mm)"""
        return self._tolerance
    
    @tolerance.setter
    def tolerance(self, value: float):
        self._tolerance = float(value)
        
    @property
    def travel_speed(self) -> float:
        """Travel speed when probing multiple points (in mm/min)"""
        return self._travel_speed
    
    @travel_speed.setter
    def travel_speed(self, value: float):
        self._travel_speed = float(value)

    @property
    def trigger_height(self) -> float:
        """Z height at which the probe is triggered (in mm)"""
        return self._trigger_height

    @trigger_height.setter
    def trigger_height(self, value: float):
        self._trigger_height = float(value)
        
    @property
    def type(self) -> ProbeType:
        """Type of the configured probe
        See also ProbeType"""
        return self._type
    
    @type.setter
    def type(self, value: ProbeType):
        if isinstance(value, ProbeType):
            self._type = value
        elif isinstance(value, int):
            self._type = ProbeType(value)
        else:
            raise TypeError(f"{__name__}.type must be of type ProbeType."
                            f" Got {type(value)}: {value}")
        
    @property
    def value(self) -> list[int]:
        """Current analog values of the probe"""
        return self._value
