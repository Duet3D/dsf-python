from __future__ import annotations

from .analog_sensor import AnalogSensor
from .endstop import Endstop
from .filament_monitors import FilamentMonitor
from .gp_input_port import GpInputPort
from .probe import Probe
from ..model_collection import ModelCollection
from ..model_object import ModelObject


class Sensors(ModelObject):
    """Information about sensors"""

    def __init__(self):
        super(Sensors, self).__init__()
        self._analog = ModelCollection(AnalogSensor)
        self._endstops = ModelCollection(Endstop)
        self._filament_monitors = ModelCollection(FilamentMonitor)
        self._gp_in = ModelCollection(GpInputPort)
        self._probes = ModelCollection(Probe)

    @property
    def analog(self) -> list[AnalogSensor]:
        """List of analog sensors"""
        return self._analog

    @property
    def endstops(self) -> list[Endstop]:
        """List of configured endstops"""
        return self._endstops

    @property
    def filament_monitors(self) -> list[FilamentMonitor]:
        """List of configured filament monitors"""
        return self._filament_monitors

    @property
    def gp_in(self) -> list[GpInputPort]:
        """List of general-purpose input ports"""
        return self._gp_in

    @property
    def probes(self) -> list[Probe]:
        """"""
        return self._probes
