from enum import Enum


class AnalogSensorType(str, Enum):
    """Enumeration of supported analog sensor types"""

    # Regular temperature thermistor
    Thermistor = "thermistor"

    # PT1000 sensor
    PT1000 = "pt1000"

    # RTD MAX31865
    MAX31865 = "rtdmax31865"

    # MAX31855 thermocouple
    MAX31855 = "thermocouplemax31855"

    # MAX31856 thermocouple
    MAX31856 = "thermocouplemax31856"

    # Linear analog sensor
    LinearAnalog = "linearanalog"

    # DHT21 sensor
    DHT21 = "dht21"

    # DHT22 sensor
    DHT22 = "dht22"

    # DHT humidity sensor
    DHTHumidity = "dhthumidity"

    # BME280 sensor
    BME280 = "bme280"

    # BME280 pressure sensor
    BME280Pressure = "bmepressure"

    # BME280 humidity sensor
    BME280Humidity = "bmehumidity"

    # BME68x temperature sensor
    BME68x = "bme68x"

    # BME68x pressure sensor
    BME68xPressure = "bme68xpressure"

    # BME68x humidity sensor
    BME68xHumidity = "bme68xhumidity"

    # BME68x gas resistance sensor
    BME68xGas = "bme68xgas"

    # Current loop sensor
    CurrentLoop = "currentloop"

    # ADS131 channel 0 (unipolar)
    ADS131Chan0Unipolar = "ads131.chan0.u"
    
    # ADS131 channel 0 (bipolar)
    ADS131Chan0Bipolar = "ads131.chan0.b"
    
    # ADS131 channel 1
    ADS131Chan1 = "ads131.chan1"

    # MCU temperature
    McuTemp = "mcutemp"

    # On-board stepper driver sensors
    Drivers = "drivers"

    # Stepper driver sensors on the DueX expansion board
    DriversDuex = "driversduex"

    # Unknown temperature sensor
    Unknown = "unknown"
