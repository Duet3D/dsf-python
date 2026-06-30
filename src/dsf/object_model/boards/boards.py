from enum import Enum

from .accelerometer import Accelerometer
from .board_closed_loop import BoardClosedLoop
from .direct_display import DirectDisplay
from .driver import Driver
from .inductive_sensor import InductiveSensor
from .min_max_current import MinMaxCurrent
from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import nullable_model_prop, model_prop


class BoardState(str, Enum):
    """
    Enumeration of possible expansion board states
    """

    # Unknown state
    unknown = "unknown"

    # Flashing new firmware
    flashing = "flashing"

    # Failed to flash new firmware
    flashFailed = "flashFailed"

    # Board is being reset
    resetting = "resetting"

    # Board is up and running
    running = "running"


class Board(ModelObject):
    """Information about a connected board"""

    # Accelerometer of this board or None if unknown
    accelerometer = nullable_model_prop('accelerometer', Accelerometer)

    # CAN address of this board or None if not applicable
    can_address = nullable_model_prop('can_address', int)

    # Closed loop data of this board or None if unknown
    closed_loop = nullable_model_prop('closed_loop', BoardClosedLoop)

    # Details about a connected display or None if none is connected
    direct_display = nullable_model_prop('direct_display', DirectDisplay)

    # Drivers of this board
    drivers = nullable_model_prop('drivers', ModelCollection[Driver], lambda: ModelCollection(Driver))

    # Date of the firmware build
    firmware_date = model_prop('firmware_date', str, "")

    # Filename of the firmware binary
    firmware_file_name = model_prop('firmware_file_name', str, "")

    # Name of the firmware build
    firmware_name = model_prop('firmware_name', str, "")

    # Version of the firmware build
    firmware_version = model_prop('firmware_version', str, "")

    # Filename of the IAP binary that is used for updates from the SBC or None if unsupported
    iap_file_name_SBC = nullable_model_prop('iap_file_name_SBC', str)

    # Filename of the IAP binary that is used for updates from the SD card or None if unsupported
    iap_file_name_SD = nullable_model_prop('iap_file_name_SD', str)

    # Amount of free RAM on this board (in bytes or null if unknown)
    free_ram = nullable_model_prop('free_ram', int)

    # Information about an inductive sensor or None if not present
    inductive_sensor = nullable_model_prop('inductive_sensor', InductiveSensor)

    # Maximum number of heaters this board can control
    max_heaters = model_prop('max_heaters', int)

    # Maximum number of motors this board can drive
    max_motors = model_prop('max_motors', int)

    # Minimum, maximum, and current temperatures of the MCU or None if unknown
    mcu_temp = nullable_model_prop('mcu_temp', MinMaxCurrent)

    # Full name of the board
    name = model_prop('name', str, "")

    # Short name of the board
    short_name = model_prop('short_name', str, "")

    # State of this board
    state = model_prop('state', BoardState, BoardState.unknown)

    # Indicates if this board supports external displays
    supports_direct_display = model_prop('supports_direct_display', bool, False)

    # Unique identifier of the board or None if unknown
    unique_id = nullable_model_prop('unique_id', str)

    # Minimum, maximum, and current voltages on the 12V rail or None if unknown
    v_12 = nullable_model_prop('v_12', MinMaxCurrent)

    # Minimum, maximum, and current voltages on the input rail or None if unknown
    v_in = nullable_model_prop('v_in', MinMaxCurrent)

    # Filename of the on-board WiFi chip or None if not present
    wifi_firmware_file_name = nullable_model_prop('wifi_firmware_file_name', str)


    def __init__(self):
        super(Board, self).__init__()
