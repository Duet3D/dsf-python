from enum import Enum


class AnalogSensorType(str, Enum):
    """Enumeration of supported analog sensor types"""

    # Regular temperature thermistor
    Thermistor = "Thermistor"

    # PT1000 sensor
    PT1000 = "PT1000"

    # RTD MAX31865
    MAX31865 = "MAX31865"

    # MAX31855 thermocouple
    MAX31855 = "MAX31855"

    # MAX31856 thermocouple
    MAX31856 = "MAX31856"

    # Linear analog sensor
    LinearAnalaog = "LinearAnalaog"

    # DHT11 sensor
    DHT11 = "DHT11"

    # DHT21 sensor
    DHT21 = "DHT21"

    # DHT22 sensor
    DHT22 = "DHT22"

    # DHT humidity sensor
    DHTHumidity = "DHTHumidity"

    # Current loop sensor
    CurrentLoop = "CurrentLoop"

    # MCU temperature
    McuTemp = "McuTemp"

    # On-board stepper driver sensors
    Drivers = "Drivers"

    # Stepper driver sensors on the DueX expansion board
    DriversDuex = "DriversDuex"

    # Unknown temperature sensor
    Unknown = "Unknown"
