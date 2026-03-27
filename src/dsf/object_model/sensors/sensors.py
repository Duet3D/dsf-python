from typing import Optional

from .analog_sensor import AnalogSensor
from .endstop import Endstop
from .filament_monitors import FilamentMonitor
from .gp_input_port import GpInputPort
from .probe import Probe
from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import model_prop


class Sensors(ModelObject):
    """Information about sensors"""

    # List of analog sensors
    analog = model_prop("analog", ModelCollection[Optional[AnalogSensor]], ModelCollection(AnalogSensor))

    # List of configured endstops
    endstops = model_prop("endstops", ModelCollection[Optional[Endstop]], ModelCollection(Endstop))

    # List of configured filament monitors
    filament_monitors = model_prop("filament_monitors", ModelCollection[Optional[FilamentMonitor]], ModelCollection(FilamentMonitor))

    # List of general-purpose input ports
    gp_in = model_prop("gp_in", ModelCollection[Optional[GpInputPort]], ModelCollection(GpInputPort))

    # List of probes
    probes = model_prop("probes", ModelCollection[Optional[Probe]], ModelCollection(Probe))

    def __init__(self):
        super(Sensors, self).__init__()
