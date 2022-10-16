from typing import List

from .analog_sensor import AnalogSensor
from .endstop import Endstop
from .filament_monitors import FilamentMonitor
from .gp_input_port import GpInputPort
from .probe import Probe
from ..model_object import ModelObject


class Sensors(ModelObject):
    """Information about sensors"""

    def __init__(self):
        super(Sensors, self).__init__()
        self._analog = []
        self._endstops = []
        self._filament_monitors = []
        self._gp_in = []
        self._probes = []

    @property
    def analog(self) -> List[AnalogSensor]:
        """List of analog sensors"""
        return self._analog

    @property
    def endstops(self) -> List[Endstop]:
        """List of configured endstops"""
        return self._endstops

    @property
    def filament_monitors(self) -> List[FilamentMonitor]:
        """List of configured filament monitors"""
        return self._filament_monitors

    @property
    def gp_in(self) -> List[GpInputPort]:
        """List of general-purpose input ports"""
        return self._gp_in

    @property
    def probes(self) -> List[Probe]:
        """"""
        return self._probes

    def _update_from_json(self, **kwargs) -> 'Sensors':
        """Override ObjectModel._update_from_json to update properties which doesn't have a setter"""
        super(Sensors, self)._update_from_json(**kwargs)
        self._analog = [AnalogSensor.from_json(item) for item in kwargs.get('analog', [])]
        self._endstops = [Endstop.from_json(item) if item else None for item in kwargs.get('endstops', [])]
        self._filament_monitors = [FilamentMonitor.from_json(item) for item in kwargs.get('filamentMonitors', [])]
        self._gp_in = [GpInputPort.from_json(item) for item in kwargs.get('gpIn', [])]
        self._probes = [Probe.from_json(item) for item in kwargs.get('probes', [])]
        return self
