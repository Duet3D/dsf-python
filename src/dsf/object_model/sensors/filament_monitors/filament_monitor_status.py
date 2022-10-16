from enum import Enum


class FilamentMonitorStatus(str, Enum):
    """Possible filament sensor status"""

    # No monitor is present
    NoMonitor = "NoMonitor"

    # Filament working normally
    Ok = "Ok"

    # No data received from the remote filament sensor
    NoDataReceived = "NoDataReceived"

    # No filament present
    NoFilament = "NoFilament"

    # Sensor reads less movement than expected
    TooLittleMovement = "TooLittleMovement"

    # Sensor reads more movment than expected
    TooMuchMovement = "TooMuchMovement"

    # Sensor encountered an error
    SensorError = "SensorError"
