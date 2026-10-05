from enum import Enum

from ...utils import DeprecatedAliasEnumType


class AnalogSensorType(str, Enum, metaclass=DeprecatedAliasEnumType):
    """Enumeration of supported analog sensor types"""

    # Regular temperature thermistor
    THERMISTOR = "thermistor"

    # PT1000 sensor
    PT1000 = "pt1000"

    # RTD MAX31865
    MAX31865 = "rtdmax31865"

    # MAX31855 thermocouple
    MAX31855 = "thermocouplemax31855"

    # MAX31856 thermocouple
    MAX31856 = "thermocouplemax31856"

    # Linear analog sensor
    LINEAR_ANALOG = "linearanalog"

    # DHT21 sensor
    DHT21 = "dht21"

    # DHT22 sensor
    DHT22 = "dht22"

    # DHT humidity sensor
    DHT_HUMIDITY = "dhthumidity"

    # BME280 sensor
    BME280 = "bme280"

    # BME280 pressure sensor
    BME280_PRESSURE = "bmepressure"

    # BME280 humidity sensor
    BME280_HUMIDITY = "bmehumidity"

    # BME68x temperature sensor
    BME68X = "bme68x"

    # BME68x pressure sensor
    BME68X_PRESSURE = "bme68xpressure"

    # BME68x humidity sensor
    BME68X_HUMIDITY = "bme68xhumidity"

    # BME68x gas resistance sensor
    BME68X_GAS = "bme68xgas"

    # Current loop sensor
    CURRENT_LOOP = "currentloop"

    # ADS131 channel 0 (unipolar)
    ADS131_CHAN0_UNIPOLAR = "ads131.chan0.u"

    # ADS131 channel 0 (bipolar)
    ADS131_CHAN0_BIPOLAR = "ads131.chan0.b"

    # ADS131 channel 1
    ADS131_CHAN1 = "ads131.chan1"

    # MCU temperature
    MCU_TEMP = "mcutemp"

    # On-board stepper driver sensors
    DRIVERS = "drivers"

    # Stepper driver sensors on the DueX expansion board
    DRIVERS_DUEX = "driversduex"

    # Sensor on a CAN-connected expansion board
    REMOTE = "remote"

    # Unknown temperature sensor
    UNKNOWN = "unknown"

    # Previous names, deprecated
    ADS131Chan0Bipolar = ADS131_CHAN0_BIPOLAR
    ADS131Chan0Unipolar = ADS131_CHAN0_UNIPOLAR
    ADS131Chan1 = ADS131_CHAN1
    BME280Humidity = BME280_HUMIDITY
    BME280Pressure = BME280_PRESSURE
    BME68x = BME68X
    BME68xGas = BME68X_GAS
    BME68xHumidity = BME68X_HUMIDITY
    BME68xPressure = BME68X_PRESSURE
    CurrentLoop = CURRENT_LOOP
    DHTHumidity = DHT_HUMIDITY
    Drivers = DRIVERS
    DriversDuex = DRIVERS_DUEX
    LinearAnalog = LINEAR_ANALOG
    McuTemp = MCU_TEMP
    Remote = REMOTE
    Thermistor = THERMISTOR
    Unknown = UNKNOWN
