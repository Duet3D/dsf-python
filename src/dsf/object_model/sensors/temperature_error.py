from enum import Enum


class TemperatureError(str, Enum):
    """Result codes returned by temperature sensor drivers"""

    # Sensor is functional
    ok = "ok"

    # Short circuit detected
    shortCircuit = "shortCircuit"

    # Short to VCC detected
    shortToVcc = "shortToVcc"

    # Short to GND detected
    shortToGround = "shortToGround"

    # Sensor circuit is open
    openCircuit = "openCircuit"

    # Timeout while waiting for sensor data
    timeout = "timeout"

    # IO error
    ioError = "ioError"

    # Hardware error
    hardwareError = "hardwareError"

    # Not ready
    notReady = "notReady"

    # Invalid output number
    invalidOutputNumber = "invalidOutputNumber"

    # Sensor bus is busy
    busBusy = "busBusy"

    # Bad sensor response
    badResponse = "badResponse"

    # Unknown sensor port
    unknownPort = "unknownPort"

    # Sensor not initialized
    notInitialised = "notInitialised"

    # Unknown sensor
    unknownSensor = "unknownSensor"

    # Sensor exceeded min/max voltage
    overOrUnderVoltage = "overOrUnderVoltage"

    # Bad VREF detected
    badVref = "badVref"

    # Bad VSSA detected
    badVssa = "badVssa"

    # Unknown error
    unknownError = "unknownError"
