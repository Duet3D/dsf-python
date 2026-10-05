from enum import Enum

from ....utils import DeprecatedAliasEnumType


class FilamentMonitorStatus(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Possible filament sensor status"""

    # No monitor is present
    NO_MONITOR = "noMonitor"

    # Filament working normally
    OK = "ok"

    # No data received from the remote filament sensor
    NO_DATA_RECEIVED = "noDataReceived"

    # No filament present
    NO_FILAMENT = "noFilament"

    # Sensor reads less movement than expected
    TOO_LITTLE_MOVEMENT = "tooLittleMovement"

    # Sensor reads more movment than expected
    TOO_MUCH_MOVEMENT = "tooMuchMovement"

    # Sensor encountered an error
    SENSOR_ERROR = "sensorError"

    # Previous names, deprecated
    NoDataReceived = NO_DATA_RECEIVED
    NoFilament = NO_FILAMENT
    NoMonitor = NO_MONITOR
    Ok = OK
    SensorError = SENSOR_ERROR
    TooLittleMovement = TOO_LITTLE_MOVEMENT
    TooMuchMovement = TOO_MUCH_MOVEMENT
