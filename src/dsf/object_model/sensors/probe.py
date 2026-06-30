from .probe_type import ProbeType
from .probe_touch_mode import ProbeTouchMode
from ..model_object import ModelObject
from ..model_collection import ModelCollection
from ..utils import model_prop, nullable_model_prop


class Probe(ModelObject):
    """Information about a configured probe"""

    calibration_temperature = model_prop('calibration_temperature', float, 0)
    deployed_by_user = model_prop('deployed_by_user', bool, False)
    disables_heaters = model_prop('disables_heaters', bool, False)
    dive_heights = model_prop('dive_heights', ModelCollection[float], ModelCollection(float, [0.0, 0.0]))
    is_calibrated = nullable_model_prop('is_calibrated', bool)
    last_stop_height = model_prop('last_stop_height', float, 0)
    max_probe_count = model_prop('max_probe_count', int, 1)
    measured_height = nullable_model_prop('measured_height', float)
    offsets = model_prop('offsets', ModelCollection[float], ModelCollection(float, [0.0, 0.0]))
    recovery_time = model_prop('recovery_time', float, 0)
    scan_coefficients = nullable_model_prop('scan_coefficients', ModelCollection[float], lambda: ModelCollection(float))
    speeds = model_prop('speeds', ModelCollection[float], ModelCollection(float, [2.0, 2.0]))
    temperature_coefficients = model_prop('temperature_coefficients', ModelCollection[float], ModelCollection(float, [0.0, 0.0]))
    threshold = model_prop('threshold', int, 500)
    tolerance = model_prop('tolerance', float, 0.03)
    touch_mode = nullable_model_prop('touch_mode', ProbeTouchMode)
    travel_speed = model_prop('travel_speed', float, 6000)
    trigger_height = model_prop('trigger_height', float, 0.7)
    type = model_prop('type', ProbeType, ProbeType.NoProbe)
    value = model_prop('value', ModelCollection[int], ModelCollection(int))

    def __init__(self):
        super(Probe, self).__init__()
