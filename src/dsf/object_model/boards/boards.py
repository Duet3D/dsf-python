from enum import Enum
from typing import List, Optional

from ...utils import DeprecatedAliasEnumType
from .board_closed_loop import BoardClosedLoop
from .direct_display import DirectDisplay
from .driver import Driver
from .inductive_sensor import InductiveSensor
from .min_max_current import MinMaxCurrent
from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import nullable_model_prop, model_prop


class BoardState(str, Enum, metaclass=DeprecatedAliasEnumType):
    """
    Enumeration of possible expansion board states
    """

    # Unknown state
    UNKNOWN = "unknown"

    # Flashing new firmware
    FLASHING = "flashing"

    # Failed to flash new firmware
    FLASH_FAILED = "flashFailed"

    # Board is being reset
    RESETTING = "resetting"

    # Board is up and running
    RUNNING = "running"

    # Board has stopped responding
    TIMED_OUT = "timedOut"

    # Previous names, deprecated
    flashFailed = FLASH_FAILED
    flashing = FLASHING
    resetting = RESETTING
    running = RUNNING
    timedOut = TIMED_OUT
    unknown = UNKNOWN


class Board(ModelObject):
    """
    Information about a connected board
    Every item of the boards list is either a MainBoard or an ExpansionBoard, which is decided by its position
    """

    # CAN address of this board or None if not applicable
    can_address = nullable_model_prop("can_address", int)

    # Drivers of this board
    drivers = nullable_model_prop("drivers", ModelCollection[Driver], lambda: ModelCollection(Driver))

    # Date of the firmware build
    firmware_date = model_prop("firmware_date", str, "")

    # Filename of the firmware binary
    firmware_file_name = model_prop("firmware_file_name", str, "")

    # Version of the firmware build
    firmware_version = model_prop("firmware_version", str, "")

    # Amount of free RAM on this board (in bytes or null if unknown)
    free_ram = nullable_model_prop("free_ram", int)

    # Maximum number of motors this board can drive
    max_motors = model_prop("max_motors", int)

    # Minimum, maximum, and current temperatures of the MCU or None if unknown
    mcu_temp = nullable_model_prop("mcu_temp", MinMaxCurrent)

    # Full name of the board
    name = model_prop("name", str, "")

    # Short name of the board
    short_name = model_prop("short_name", str, "")

    # Unique identifier of the board or None if unknown
    unique_id = nullable_model_prop("unique_id", str)

    # Minimum, maximum, and current voltages on the 12V rail or None if unknown
    v_12 = nullable_model_prop("v_12", MinMaxCurrent)

    # Minimum, maximum, and current voltages on the input rail or None if unknown
    v_in = nullable_model_prop("v_in", MinMaxCurrent)

    def __init__(self):
        super(Board, self).__init__()


class MainBoard(Board):
    """Information about the mainboard, which is always the first item of the boards list"""

    # Details about a connected display or None if none is connected
    direct_display = nullable_model_prop("direct_display", DirectDisplay)

    # Name of the firmware build
    firmware_name = model_prop("firmware_name", str, "")

    # Filename of the IAP binary that is used for updates from the SBC or None if unsupported
    iap_file_name_SBC = nullable_model_prop("iap_file_name_SBC", str)

    # Filename of the IAP binary that is used for updates from the SD card or None if unsupported
    iap_file_name_SD = nullable_model_prop("iap_file_name_SD", str)

    # Maximum number of heaters this board can control
    max_heaters = model_prop("max_heaters", int)

    # Indicates if this board supports external displays
    supports_direct_display = model_prop("supports_direct_display", bool, False)

    # Filename of the on-board WiFi chip or None if not present
    wifi_firmware_file_name = nullable_model_prop("wifi_firmware_file_name", str)

    def __init__(self):
        super(MainBoard, self).__init__()


class ExpansionBoard(Board):
    """Information about an expansion board connected over CAN"""

    # Closed loop data of this board or None if unknown
    closed_loop = nullable_model_prop("closed_loop", BoardClosedLoop)

    # Information about an inductive sensor or None if not present
    inductive_sensor = nullable_model_prop("inductive_sensor", InductiveSensor)

    # State of this board
    state = model_prop("state", BoardState, BoardState.UNKNOWN)

    # Connection timeout of this board (in s)
    timeout = model_prop("timeout", int, 10)

    def __init__(self):
        super(ExpansionBoard, self).__init__()


class Boards(ModelCollection[Board]):
    """
    List of connected boards.
    The first board is the mainboard, every other one is an expansion board connected over CAN
    """

    def __init__(self, value: Optional[List[Board]] = None):
        super(Boards, self).__init__(Board, value)

    def _create_item(self, index: int) -> Board:
        return MainBoard() if index == 0 else ExpansionBoard()
