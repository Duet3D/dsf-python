from ..model_object import ModelObject
from ..model_collection import ModelCollection
from ..utils import model_prop, nullable_model_prop


class FanThermostaticControl(ModelObject):
    """Thermostatic parameters of a fan"""

    # List of heaters to monitor (indices)
    # deprecated
    heaters = model_prop("heaters", ModelCollection[int], ModelCollection(int))

    # Upper temperature range required to turn on the fan (in C)
    high_temperature = nullable_model_prop("high_temperature", float)

    # Lower temperature range required to turn on the fan (in C)
    low_temperature = nullable_model_prop("low_temperature", float)

    # List of sensors to monitor (indices)
    sensors = model_prop("sensors", ModelCollection[int], ModelCollection(int))

    def __init__(self):
        super().__init__()
