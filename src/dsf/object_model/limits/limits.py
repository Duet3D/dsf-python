from ..model_object import ModelObject
from ..utils import nullable_model_prop


class Limits(ModelObject):
    """Machine configuration limits"""

    # Maximum number of axes or null if unknown
    axes = nullable_model_prop("axes", int)
    # Maximum number of axes + extruders or null if unknown
    axes_plus_extruders = nullable_model_prop("axes_plus_extruders", int)
    # Maximum number of bed heaters or null if unknown
    bed_heaters = nullable_model_prop("bed_heaters", int)
    # Maximum number of boards or null if unknown
    boards = nullable_model_prop("boards", int)
    # Maximum number of chamber heaters or null if unknown
    chamber_heaters = nullable_model_prop("chamber_heaters", int)
    # Maximum number of drivers or null if unknown
    drivers = nullable_model_prop("drivers", int)
    # Maximum number of drivers per axis or null if unknown
    drivers_per_axis = nullable_model_prop("drivers_per_axis", int)
    # Maximum number of extruders or null if unknown
    extruders = nullable_model_prop("extruders", int)
    # Maximum number of extruders per tool or null if unknown
    extruders_per_tool = nullable_model_prop("extruders_per_tool", int)
    # Maximum number of fans or null if unknown
    fans = nullable_model_prop("fans", int)
    # Maximum number of general-purpose input ports or null if unknown
    gp_in_ports = nullable_model_prop("gp_in_ports", int)
    # Maximum number of general-purpose output ports or null if unknown
    gp_out_ports = nullable_model_prop("gp_out_ports", int)
    # Maximum number of heaters or null if unknown
    heaters = nullable_model_prop("heaters", int)
    # Maximum number of heaters per tool or null if unknown
    heaters_per_tool = nullable_model_prop("heaters_per_tool", int)
    # Maximum number of configured LED strips or null if unknown
    led_strips = nullable_model_prop("led_strips", int)
    # Maximum number of monitors per heater or null if unknown
    monitors_per_heater = nullable_model_prop("monitors_per_heater", int)
    # Maximum number of output ports per heater or null if unknown
    ports_per_heater = nullable_model_prop("ports_per_heater", int)
    # Maximum number of axes reported when the move key is requested
    reported_move_axes = nullable_model_prop("reported_move_axes", int)
    # Maximum number of restore points or null if unknown
    restore_points = nullable_model_prop("restore_points", int)
    # Maximum number of sensors or null if unknown
    sensors = nullable_model_prop("sensors", int)
    # Maximum number of spindles or null if unknown
    spindles = nullable_model_prop("spindles", int)
    # Maximum number of tools or null if unknown
    tools = nullable_model_prop("tools", int)
    # Maximum number of tracked objects or null if unknown
    tracked_objects = nullable_model_prop("tracked_objects", int)
    # Maximum number of triggers or null if unknown
    triggers = nullable_model_prop("triggers", int)
    # Maximum number of volumes or null if unknown
    volumes = nullable_model_prop("volumes", int)
    # Maximum number of workplaces or null if unknown
    workplaces = nullable_model_prop("workplaces", int)
    # Maximum number of Z-probe programming bytes or null if unknown
    z_probe_program_bytes = nullable_model_prop("z_probe_program_bytes", int)
    # Maximum number of Z-probes or null if unknown
    z_probes = nullable_model_prop("z_probes", int)

    def __init__(self):
        super().__init__()
        self._axes = None
        self._axes_plus_extruders = None
        self._bed_heaters = None
        self._boards = None
        self._chamber_heaters = None
        self._drivers = None
        self._drivers_per_axis = None
        self._extruders = None
        self._extruders_per_tool = None
        self._fans = None
        self._gp_in_ports = None
        self._gp_out_ports = None
        self._heaters = None
        self._heaters_per_tool = None
        self._led_strips = None
        self._monitors_per_heater = None
        self._ports_per_heater = None
        self._restore_points = None
        self._sensors = None
        self._spindles = None
        self._tools = None
        self._tracked_objects = None
        self._triggers = None
        self._volumes = None
        self._workplaces = None
        self._z_probe_program_bytes = None
        self._z_probes = None
