from typing import Union

from ..model_object import ModelObject


class Limits(ModelObject):
    """Machine configuration limits"""

    def __init__(self):
        super().__init__()
        # Maximum number of axes or null if unknown
        self._axes = None
        # Maximum number of axes + extruders or null if unknown
        self._axes_plus_extruders = None
        # Maximum number of bed heaters or null if unknown
        self._bed_heaters = None
        # Maximum number of boards or null if unknown
        self._boards = None
        # Maximum number of chamber heaters or null if unknown
        self._chamber_heaters = None
        # Maximum number of drivers or null if unknown
        self._drivers = None
        # Maximum number of drivers per axis or null if unknown
        self._drivers_per_axis = None
        # Maximum number of extruders or null if unknown
        self._extruders = None
        # Maximum number of extruders per tool or null if unknown
        self._extruders_per_tool = None
        # Maximum number of fans or null if unknown
        self._fans = None
        # Maximum number of general-purpose input ports or null if unknown
        self._gp_in_ports = None
        # Maximum number of general-purpose output ports or null if unknown
        self._gp_out_ports = None
        # Maximum number of heaters or null if unknown
        self._heaters = None
        # Maximum number of heaters per tool or null if unknown
        self._heaters_per_tool = None
        # Maximum number of monitors per heater or null if unknown
        self._monitors_per_heater = None
        # Maximum number of restore points or null if unknown
        self._restore_points = None
        # Maximum number of sensors or null if unknown
        self._sensors = None
        # Maximum number of spindles or null if unknown
        self._spindles = None
        # Maximum number of tools or null if unknown
        self._tools = None
        # Maximum number of tracked objects or null if unknown
        self._tracked_objects = None
        # Maximum number of triggers or null if unknown
        self._triggers = None
        # Maximum number of volumes or null if unknown
        self._volumes = None
        # Maximum number of workplaces or null if unknown
        self._workplaces = None
        # Maximum number of Z-probe programming bytes or null if unknown
        self._z_probe_program_bytes = None
        # Maximum number of Z-probes or null if unknown
        self._z_probes = None

    @property
    def axes(self) -> Union[int, None]:
        """Maximum number of axes or null if unknown"""
        return self._axes

    @axes.setter
    def axes(self, value):
        self._axes = int(value) if value is not None else None

    @property
    def axes_plus_extruders(self) -> Union[int, None]:
        """Maximum number of axes + extruders or null if unknown"""
        return self._axes_plus_extruders

    @axes_plus_extruders.setter
    def axes_plus_extruders(self, value):
        self._axes_plus_extruders = int(value) if value is not None else None

    @property
    def bed_heaters(self) -> Union[int, None]:
        """Maximum number of bed heaters or null if unknown"""
        return self._bed_heaters

    @bed_heaters.setter
    def bed_heaters(self, value):
        self._bed_heaters = int(value) if value is not None else None

    @property
    def boards(self) -> Union[int, None]:
        """Maximum number of boards or null if unknown"""
        return self._boards

    @boards.setter
    def boards(self, value):
        self._boards = int(value) if value is not None else None

    @property
    def chamber_heaters(self) -> Union[int, None]:
        """Maximum number of chamber heaters or null if unknown"""
        return self._chamber_heaters

    @chamber_heaters.setter
    def chamber_heaters(self, value):
        self._chamber_heaters = int(value) if value is not None else None

    @property
    def drivers(self) -> Union[int, None]:
        """Maximum number of drivers or null if unknown"""
        return self._drivers

    @drivers.setter
    def drivers(self, value):
        self._drivers = int(value) if value is not None else None

    @property
    def drivers_per_axis(self) -> Union[int, None]:
        """Maximum number of drivers per axis or null if unknown"""
        return self._drivers_per_axis

    @drivers_per_axis.setter
    def drivers_per_axis(self, value):
        self._drivers_per_axis = int(value) if value is not None else None

    @property
    def extruders(self) -> Union[int, None]:
        """Maximum number of extruders or null if unknown"""
        return self._extruders

    @extruders.setter
    def extruders(self, value):
        self._extruders = int(value) if value is not None else None

    @property
    def extruders_per_tool(self) -> Union[int, None]:
        """Maximum number of extruders per tool or null if unknown"""
        return self._extruders_per_tool

    @extruders_per_tool.setter
    def extruders_per_tool(self, value):
        self._extruders_per_tool = int(value) if value is not None else None

    @property
    def fans(self) -> Union[int, None]:
        """Maximum number of fans or null if unknown"""
        return self._fans

    @fans.setter
    def fans(self, value):
        self._fans = int(value) if value is not None else None

    @property
    def gp_in_ports(self) -> Union[int, None]:
        """Maximum number of general-purpose input ports or null if unknown"""
        return self._gp_in_ports

    @gp_in_ports.setter
    def gp_in_ports(self, value):
        self._gp_in_ports = int(value) if value is not None else None

    @property
    def gp_out_ports(self) -> Union[int, None]:
        """Maximum number of general-purpose output ports or null if unknown"""
        return self._gp_out_ports

    @gp_out_ports.setter
    def gp_out_ports(self, value):
        self._gp_out_ports = int(value) if value is not None else None

    @property
    def heaters(self) -> Union[int, None]:
        """Maximum number of heaters or null if unknown"""
        return self._heaters

    @heaters.setter
    def heaters(self, value):
        self._heaters = int(value) if value is not None else None

    @property
    def heaters_per_tool(self) -> Union[int, None]:
        """Maximum number of heaters per tool or null if unknown"""
        return self._heaters_per_tool

    @heaters_per_tool.setter
    def heaters_per_tool(self, value):
        self._heaters_per_tool = int(value) if value is not None else None

    @property
    def monitors_per_heater(self) -> Union[int, None]:
        """Maximum number of monitors per heater or null if unknown"""
        return self._monitors_per_heater

    @monitors_per_heater.setter
    def monitors_per_heater(self, value):
        self._monitors_per_heater = int(value) if value is not None else None

    @property
    def restore_points(self) -> Union[int, None]:
        """Maximum number of restore points or null if unknown"""
        return self._restore_points

    @restore_points.setter
    def restore_points(self, value):
        self._restore_points = int(value) if value is not None else None

    @property
    def sensors(self) -> Union[int, None]:
        """Maximum number of sensors or null if unknown"""
        return self._sensors

    @sensors.setter
    def sensors(self, value):
        self._sensors = int(value) if value is not None else None

    @property
    def spindles(self) -> Union[int, None]:
        """Maximum number of spindles or null if unknown"""
        return self._spindles

    @spindles.setter
    def spindles(self, value):
        self._spindles = int(value) if value is not None else None

    @property
    def tools(self) -> Union[int, None]:
        """Maximum number of tools or null if unknown"""
        return self._tools

    @tools.setter
    def tools(self, value):
        self._tools = int(value) if value is not None else None

    @property
    def tracked_objects(self) -> Union[int, None]:
        """Maximum number of tracked objects or null if unknown"""
        return self._tracked_objects

    @tracked_objects.setter
    def tracked_objects(self, value):
        self._tracked_objects = int(value) if value is not None else None

    @property
    def triggers(self) -> Union[int, None]:
        """Maximum number of triggers or null if unknown"""
        return self._triggers

    @triggers.setter
    def triggers(self, value):
        self._triggers = int(value) if value is not None else None

    @property
    def volumes(self) -> Union[int, None]:
        """Maximum number of triggers or null if unknown"""
        return self._volumes

    @volumes.setter
    def volumes(self, value):
        self._volumes = int(value) if value is not None else None

    @property
    def workplaces(self) -> Union[int, None]:
        """Maximum number of workplaces or null if unknown"""
        return self._workplaces

    @workplaces.setter
    def workplaces(self, value):
        self._workplaces = int(value) if value is not None else None

    @property
    def z_probe_program_bytes(self) -> Union[int, None]:
        """Maximum number of Z-probe programming bytes or null if unknown"""
        return self._z_probe_program_bytes

    @z_probe_program_bytes.setter
    def z_probe_program_bytes(self, value):
        self._z_probe_program_bytes = int(value) if value is not None else None

    @property
    def z_probes(self) -> Union[int, None]:
        """Maximum number of Z-probes or null if unknown"""
        return self._z_probes

    @z_probes.setter
    def z_probes(self, value):
        self._z_probes = int(value) if value is not None else None
