from enum import Enum


class FilamentMonitorStatus(str, Enum):
    """Possible filament sensor status"""

    # No monitor is present
    NoMonitor = "noMonitor"

    # Filament working normally
    Ok = "ok"

    # No data received from the remote filament sensor
    NoDataReceived = "noDataReceived"

    # No filament present
    NoFilament = "noFilament"

    # Sensor reads less movement than expected
    TooLittleMovement = "tooLittleMovement"

    # Sensor reads more movment than expected
    TooMuchMovement = "tooMuchMovement"

    # Sensor encountered an error
    SensorError = "sensorError"
