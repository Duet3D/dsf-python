from enum import Enum

from ...utils import DeprecatedAliasEnumType


class TemperatureError(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Result codes returned by temperature sensor drivers"""

    # Sensor is functional
    OK = "ok"

    # Short circuit detected
    SHORT_CIRCUIT = "shortCircuit"

    # Short to VCC detected
    SHORT_TO_VCC = "shortToVcc"

    # Short to GND detected
    SHORT_TO_GROUND = "shortToGround"

    # Sensor circuit is open
    OPEN_CIRCUIT = "openCircuit"

    # Timeout while waiting for sensor data
    TIMEOUT = "timeout"

    # IO error
    IO_ERROR = "ioError"

    # Hardware error
    HARDWARE_ERROR = "hardwareError"

    # Not ready
    NOT_READY = "notReady"

    # Invalid output number
    INVALID_OUTPUT_NUMBER = "invalidOutputNumber"

    # Sensor bus is busy
    BUS_BUSY = "busBusy"

    # Bad sensor response
    BAD_RESPONSE = "badResponse"

    # Unknown sensor port
    UNKNOWN_PORT = "unknownPort"

    # Sensor not initialized
    NOT_INITIALISED = "notInitialised"

    # Unknown sensor
    UNKNOWN_SENSOR = "unknownSensor"

    # Sensor exceeded min/max voltage
    OVER_OR_UNDER_VOLTAGE = "overOrUnderVoltage"

    # Bad VREF detected
    BAD_VREF = "badVref"

    # Bad VSSA detected
    BAD_VSSA = "badVssa"

    # Sensor reading too low
    READING_TOO_LOW = "readingTooLow"

    # Sensor reading too high
    READING_TOO_HIGH = "readingTooHigh"

    # Ambient reading too low (for composite sensors that read ambient temperature to calculate object temperature)
    AMBIENT_READING_TOO_LOW = "ambientReadingTooLow"

    # Ambient reading too high (for composite sensors that read ambient temperature to calculate object temperature)
    AMBIENT_READING_TOO_HIGH = "ambientReadingTooHigh"

    # Unknown error
    UNKNOWN_ERROR = "unknownError"

    # Previous names, deprecated
    ambientReadingTooHigh = AMBIENT_READING_TOO_HIGH
    ambientReadingTooLow = AMBIENT_READING_TOO_LOW
    badResponse = BAD_RESPONSE
    badVref = BAD_VREF
    badVssa = BAD_VSSA
    busBusy = BUS_BUSY
    hardwareError = HARDWARE_ERROR
    invalidOutputNumber = INVALID_OUTPUT_NUMBER
    ioError = IO_ERROR
    notInitialised = NOT_INITIALISED
    notReady = NOT_READY
    ok = OK
    openCircuit = OPEN_CIRCUIT
    overOrUnderVoltage = OVER_OR_UNDER_VOLTAGE
    readingTooHigh = READING_TOO_HIGH
    readingTooLow = READING_TOO_LOW
    shortCircuit = SHORT_CIRCUIT
    shortToGround = SHORT_TO_GROUND
    shortToVcc = SHORT_TO_VCC
    timeout = TIMEOUT
    unknownError = UNKNOWN_ERROR
    unknownPort = UNKNOWN_PORT
    unknownSensor = UNKNOWN_SENSOR
