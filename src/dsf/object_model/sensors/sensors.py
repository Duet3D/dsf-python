from typing import Sequence

from .analog_sensor import AnalogSensor
from .endstop import Endstop
from .filament_monitors import FilamentMonitor
from .gp_input_port import GpInputPort
from .probe import Probe
from ..model_collection import ModelCollection
from ..model_object import ModelObject


class Sensors(ModelObject):
    """Information about sensors"""

    def __init__(self) -> None:
        super(Sensors, self).__init__()
        self._analog: ModelCollection[AnalogSensor] = ModelCollection(AnalogSensor)
        self._endstops: ModelCollection[Endstop] = ModelCollection(Endstop)
        self._filament_monitors: ModelCollection[FilamentMonitor] = ModelCollection(FilamentMonitor)
        self._gp_in: ModelCollection[GpInputPort] = ModelCollection(GpInputPort)
        self._probes: ModelCollection[Probe] = ModelCollection(Probe)

    @property
    def analog(self) -> Sequence[AnalogSensor | None]:
        """List of analog sensors"""
        return self._analog

    @property
    def endstops(self) -> Sequence[Endstop | None]:
        """List of configured endstops"""
        return self._endstops

    @property
    def filament_monitors(self) -> Sequence[FilamentMonitor | None]:
        """List of configured filament monitors"""
        return self._filament_monitors

    @property
    def gp_in(self) -> Sequence[GpInputPort | None]:
        """List of general-purpose input ports"""
        return self._gp_in

    @property
    def probes(self) -> Sequence[Probe | None]:
        """"""
        return self._probes
