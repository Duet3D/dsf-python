from typing import List, Optional, Sequence

from .probe_type import ProbeType
from ..model_object import ModelObject
from ...utils import deprecated


class Probe(ModelObject):
    """Information about a configured probe"""

    def __init__(self) -> None:
        super(Probe, self).__init__()
        self._calib_a: Optional[float] = None
        self._calib_b: Optional[float] = None
        self._calibration_temperature: float = 0
        self._deployed_by_user: bool = False
        self._disables_heaters: bool = False
        self._dive_height: float = 5
        self._dive_heights: List[float] = [0.0, 0.0]
        self._is_calibrated: Optional[bool] = None
        self._last_stop_height: float = 0
        self._max_probe_count: int = 1
        self._measured_height: Optional[float] = None
        self._offsets: List[float] = [0.0, 0.0]
        self._recovery_time: float = 0
        self._scan_coefficients: Optional[List[float]] = None
        self._speeds: List[float] = [2.0, 2.0]
        self._temperature_coefficients: List[float] = [0.0, 0.0]
        self._threshold: int = 500
        self._tolerance: float = 0.03
        self._travel_speed: float = 6000
        self._trigger_height: float = 0.7
        self._type: ProbeType = ProbeType.NoProbe
        self._value: List[int] = []

    @property
    def calib_a(self) -> Optional[float]:
        """Linear coefficient for scanning probes"""
        return self._calib_a

    @calib_a.setter
    def calib_a(self, value: Optional[float | int | str]):
        self._calib_a = float(value) if value is not None else None

    @property
    def calib_b(self) -> Optional[float]:
        """Quadratic coefficient for scanning probes"""
        return self._calib_b

    @calib_b.setter
    def calib_b(self, value: Optional[float | int | str]):
        self._calib_b = float(value) if value is not None else None

    @property
    def calibration_temperature(self) -> float:
        """Calibration temperature (in C)"""
        return self._calibration_temperature

    @calibration_temperature.setter
    def calibration_temperature(self, value: float | int | str):
        self._calibration_temperature = float(value)
        
    @property
    def deployed_by_user(self) -> bool:
        """Indicates if the user has deployed the probe"""
        return self._deployed_by_user
    
    @deployed_by_user.setter
    def deployed_by_user(self, value: bool | int | str):
        self._deployed_by_user = bool(value)
        
    @property
    def disables_heaters(self) -> bool:
        """Whether probing disables the heater(s)"""
        return self._disables_heaters
    
    @disables_heaters.setter
    def disables_heaters(self, value: bool | int | str):
        self._disables_heaters = bool(value)
        
    @property
    @deprecated(f"Use {__name__}.dive_heights[0] instead")
    def dive_height(self) -> float:
        """Dive height (in mm)
        Deprecated: Use dive_heights[0] instead
        """
        return self._dive_height
    
    @dive_height.setter
    def dive_height(self, value: float | int | str):
        self._dive_height = float(value)

    @property
    def dive_heights(self) -> List[float]:
        """Dive heights of the probe.
        The first element is the regular dive height, the second element may be used by scanning Z-probes
        """
        return self._dive_heights

    @property
    def is_calibrated(self) -> Optional[bool]:
        """Indicates if the scanning probe is calibrated"""
        return self._is_calibrated

    @is_calibrated.setter
    def is_calibrated(self, value: Optional[bool | int | str]):
        self._is_calibrated = bool(value) if value is not None else None
        
    @property
    def last_stop_height(self) -> float:
        """Height of the probe where it stopped last time (in mm)"""
        return self._last_stop_height
    
    @last_stop_height.setter
    def last_stop_height(self, value: float | int | str):
        self._last_stop_height = float(value)
        
    @property
    def max_probe_count(self) -> int:
        """Maximum number of times to probe after a bad reading was determined"""
        return self._max_probe_count
    
    @max_probe_count.setter
    def max_probe_count(self, value: int | str):
        self._max_probe_count = int(value)
        
    @property
    def measured_height(self) -> Optional[float]:
        """Measured height (only applicable for scanning probes, in mm or null)"""
        return self._measured_height
    
    @measured_height.setter
    def measured_height(self, value: Optional[float | int | str]):
        self._measured_height = None if value is None else float(value)
        
    @property
    def offsets(self) -> List[float]:
        """X+Y offsets (in mm)"""
        return self._offsets
    
    @property
    def recovery_time(self) -> float:
        """Recovery time (in s)"""
        return self._recovery_time
    
    @recovery_time.setter
    def recovery_time(self, value: float | int | str):
        self._recovery_time = float(value)
        
    @property
    def speed(self) -> float:
        """Probe speed (in mm/s)
        Obsolete: Use Speeds[0] instead"""
        return self._speeds[0]

    @property
    def scan_coefficients(self) -> Optional[List[float]]:
        """Coefficients for the scanning Z-probe (4 elements, if applicable)"""
        return self._scan_coefficients

    @scan_coefficients.setter
    def scan_coefficients(self, value: Optional[Sequence[float | int | str]]):
        self._scan_coefficients = None if value is None else [float(v) for v in value]
        
    @property
    def speeds(self) -> List[float]:
        """Fast and slow probing speeds (in mm/s)
        Scanning probes may have three speeds where the last one is the movement speed while probing heightmaps"""
        return self._speeds
    
    @speeds.setter
    def speeds(self, values: Sequence[float | int | str]):
        self._speeds = [float(value) for value in values]
        
    @property
    def temperature_coefficients(self) -> List[float]:
        """List of temperature coefficients"""
        return self._temperature_coefficients
        
    @property
    def threshold(self) -> int:
        """Configured trigger threshold (0..1023)"""
        return self._threshold
    
    @threshold.setter
    def threshold(self, value: int | str):
        self._threshold = int(value)
        
    @property
    def tolerance(self) -> float:
        """Allowed tolerance deviation between two measures (in mm)"""
        return self._tolerance
    
    @tolerance.setter
    def tolerance(self, value: float | int | str):
        self._tolerance = float(value)
        
    @property
    def travel_speed(self) -> float:
        """Travel speed when probing multiple points (in mm/min)"""
        return self._travel_speed
    
    @travel_speed.setter
    def travel_speed(self, value: float | int | str):
        self._travel_speed = float(value)

    @property
    def trigger_height(self) -> float:
        """Z height at which the probe is triggered (in mm)"""
        return self._trigger_height

    @trigger_height.setter
    def trigger_height(self, value: float | int | str):
        self._trigger_height = float(value)
        
    @property
    def type(self) -> ProbeType:
        """Type of the configured probe
        See also ProbeType"""
        return self._type
    
    @type.setter
    def type(self, value: Optional[ProbeType | int]):
        if value is None:
            self._type = ProbeType.NoProbe
        elif isinstance(value, ProbeType):
            self._type = value
        elif isinstance(value, int):
            self._type = ProbeType(value)
        else:
            raise TypeError(f"{__name__}.type must be of type ProbeType or None. Got {type(value)}: {value}")
        
    @property
    def value(self) -> List[int]:
        """Current analog values of the probe"""
        return self._value
