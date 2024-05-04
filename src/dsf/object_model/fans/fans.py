from .fan_thermostatic_control import FanThermostaticControl
from ..model_object import ModelObject


class Fan(ModelObject):
    """Class representing information about an attached fan"""
    def __init__(self):
        super().__init__()
        # Value of this fan (0..1 or -1 if unknown)
        self._actual_value = 0
        # Blip value indicating how long the fan is supposed to run at 100%
        # when turning it on to get it started (in s)
        self._blip = 0.1
        # Configured frequency of this fan (in Hz)
        self._frequency = 250
        # Maximum value of this fan (0..1)
        self._max = 1
        # Minimum value of this fan (0..1)
        self._min = 0
        # Name of the fan
        self._name = ""
        # Requested value for this fan on a scale between 0 and 1
        self._requested_value = 0
        # Current RPM of this fan or -1 if unknown/unset
        self._rpm = -1
        # Pulses per tacho revolution
        self._tacho_ppr = 2.0
        # Thermostatic control parameters
        self._thermostatic = FanThermostaticControl()

    @property
    def actual_value(self) -> float:
        """Value of this fan (0..1 or -1 if unknown)"""
        return self._actual_value

    @actual_value.setter
    def actual_value(self, value):
        self._actual_value = float(value)

    @property
    def blip(self) -> float:
        """Blip value indicating how long the fan is supposed to run at 100%
        when turning it on to get it started (in s)"""
        return self._blip

    @blip.setter
    def blip(self, value):
        self._blip = float(value)

    @property
    def frequency(self) -> float:
        """Configured frequency of this fan (in Hz)"""
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = float(value)

    @property
    def max(self) -> float:
        """Maximum value of this fan (0..1)"""
        return self._max

    @max.setter
    def max(self, value):
        self._max = float(value)

    @property
    def min(self) -> float:
        """Minimum value of this fan (0..1)"""
        return self._min

    @min.setter
    def min(self, value):
        self._min = float(value)

    @property
    def name(self) -> str:
        """Name of the fan"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    @property
    def requested_value(self) -> float:
        """Requested value for this fan on a scale between 0 and 1"""
        return self._requested_value

    @requested_value.setter
    def requested_value(self, value):
        self._requested_value = float(value)

    @property
    def rpm(self) -> int:
        """Current RPM of this fan or -1 if unknown/unset"""
        return self._rpm

    @rpm.setter
    def rpm(self, value):
        self._rpm = int(value)

    @property
    def tacho_ppr(self) -> float:
        """Pulses per tacho revolution"""
        return self._tacho_ppr

    @tacho_ppr.setter
    def tacho_ppr(self, value):
        self._tacho_ppr = float(value)

    @property
    def thermostatic(self) -> FanThermostaticControl:
        """Thermostatic control parameters"""
        return self._thermostatic
