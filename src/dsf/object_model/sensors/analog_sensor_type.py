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

    # DHT11 sensor
    DHT11 = "dht11"

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

    # Current loop sensor
    CurrentLoop = "currentlooppyro"

    # MCU temperature
    McuTemp = "mcutemp"

    # On-board stepper driver sensors
    Drivers = "drivers"

    # Stepper driver sensors on the DueX expansion board
    DriversDuex = "driversduex"

    # Unknown temperature sensor
    Unknown = "unknown"
