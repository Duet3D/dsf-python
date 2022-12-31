from enum import Enum
from typing import Union

from .accelerometer import Accelerometer
from .closed_loop import ClosedLoop
from .direct_display import DirectDisplay
from .min_max_current import MinMaxCurrent
from ..model_object import ModelObject
from ..utils import wrap_model_property


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

    # Accelerometer of this board or null if unknown
    accelerometer = wrap_model_property('accelerometer', Accelerometer)
    # Closed loop data of this board or null if unknown
    closed_loop = wrap_model_property('closed_loop', ClosedLoop)
    # Details about a connected display or null if none is connected
    direct_display = wrap_model_property('direct_display', DirectDisplay)
    # Minimum, maximum, and current temperatures of the MCU or null if unknown
    mcu_temp = wrap_model_property('mcu_temp', MinMaxCurrent)
    # Minimum, maximum, and current voltages on the 12V rail or null if unknown
    v_12 = wrap_model_property('v_12', MinMaxCurrent)
    # Minimum, maximum, and current voltages on the input rail or null if unknown
    v_in = wrap_model_property('v_in', MinMaxCurrent)

    def __init__(self):
        super(Board, self).__init__()

        # Accelerometer of this board or null if unknown
        self._accelerometer = None
        # Filename of the bootloader binary or null if unknown
        self._bootloader_file_name = None
        # CAN address of this board or null if not applicable
        self._can_address = None
        # Closed loop data of this board or null if unknown
        self._closed_loop = None
        # Details about a connected display or null if none is connected
        self._direct_display = None
        # Date of the firmware build
        self._firmware_date = ""
        # Filename of the firmware binary
        self._firmware_file_name = ""
        # Name of the firmware build
        self._firmware_name = ""
        # Version of the firmware build
        self._firmware_version = ""
        # Filename of the IAP binary that is used for updates from the SBC or null if unsupported
        self._iap_file_name_SBC = None
        # Filename of the IAP binary that is used for updates from the SD card or null if unsupported
        # This is only available for the mainboard (first board item)
        self._iap_file_name_SD = None
        # Maximum number of heaters this board can control
        self._max_heaters = 0
        # Maximum number of motors this board can drive
        self._max_motors = 0
        # Minimum, maximum, and current temperatures of the MCU or null if unknown
        self._mcu_temp = None
        # Full name of the board
        self._name = ""
        # Short name of this board
        self._short_name = ""
        # State of this board
        self._state = BoardState.unknown
        # Indicates if this board supports external 12864 displays
        # obsolete: Replaced with SupportsDirectDisplay
        self._supports_12864 = False
        # Indicates if this board supports external displays
        self._supports_direct_display = False
        # Unique identifier of the board or null if unknown
        self._unique_id = None
        # Minimum, maximum, and current voltages on the 12V rail or null if unknown
        self._v_12 = None
        # Minimum, maximum, and current voltages on the input rail or null if unknown
        self._v_in = None

    @property
    def bootloader_file_name(self) -> Union[str, None]:
        """Filename of the bootloader binary or null if unknown"""
        return self._bootloader_file_name

    @bootloader_file_name.setter
    def bootloader_file_name(self, value):
        self._bootloader_file_name = str(value) if value is not None else None

    @property
    def can_address(self) -> Union[int, None]:
        """CAN address of this board or null if not applicable"""
        return self._can_address

    @can_address.setter
    def can_address(self, value):
        self._can_address = int(value) if value is not None else None

    @property
    def firmware_date(self) -> str:
        """Date of the firmware build"""
        return self._firmware_date

    @firmware_date.setter
    def firmware_date(self, value):
        self._firmware_date = str(value) if value is not None else ""

    @property
    def firmware_file_name(self) -> str:
        """Filename of the firmware binary"""
        return self._firmware_file_name

    @firmware_file_name.setter
    def firmware_file_name(self, value):
        self._firmware_file_name = str(value) if value is not None else ""

    @property
    def firmware_name(self) -> str:
        """Name of the firmware build"""
        return self._firmware_name

    @firmware_name.setter
    def firmware_name(self, value):
        self._firmware_name = str(value) if value is not None else ""

    @property
    def firmware_version(self) -> str:
        """Version of the firmware build"""
        return self._firmware_version

    @firmware_version.setter
    def firmware_version(self, value):
        self._firmware_version = str(value) if value is not None else ""

    @property
    def iap_file_name_SBC(self) -> Union[str, None]:
        """Filename of the IAP binary that is used for updates from the SBC or null if unsupported"""
        return self._iap_file_name_SBC

    @iap_file_name_SBC.setter
    def iap_file_name_SBC(self, value):
        self._iap_file_name_SBC = str(value) if value is not None else None

    @property
    def iap_file_name_SD(self) -> Union[str, None]:
        """Filename of the IAP binary that is used for updates from the SD card or null if unsupported
        This is only available for the mainboard (first board item)"""
        return self._iap_file_name_SD

    @iap_file_name_SD.setter
    def iap_file_name_SD(self, value):
        self._iap_file_name_SD = str(value) if value is not None else None

    @property
    def max_heaters(self) -> int:
        """Maximum number of heaters this board can drive"""
        return self._max_heaters

    @max_heaters.setter
    def max_heaters(self, value):
        self._max_heaters = int(value) if value is not None else 0

    @property
    def max_motors(self) -> int:
        """Maximum number of motors this board can drive"""
        return self._max_motors

    @max_motors.setter
    def max_motors(self, value):
        self._max_motors = int(value) if value is not None else 0

    @property
    def name(self) -> str:
        """Full name of the board"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value) if value is not None else ""

    @property
    def short_name(self) -> str:
        """Short name of this board"""
        return self._short_name

    @short_name.setter
    def short_name(self, value):
        self._short_name = str(value) if value is not None else ""

    @property
    def state(self) -> BoardState:
        """State of this board"""
        return self._state

    @state.setter
    def state(self, value):
        if value is None or isinstance(value, BoardState):
            self._state = value
        elif isinstance(value, str):
            self._state = BoardState(value)
        else:
            raise TypeError(f"{__name__}.state must be of type BoardState or None. Got {type(value)}: {value}")

    @property
    def supports_12864(self) -> bool:
        """Indicates if this board supports external 12864 displays
        Obsolete: Replaced with SupportsDirectDisplay"""
        return self._supports_12864

    @supports_12864.setter
    def supports_12864(self, value):
        self._supports_12864 = bool(value)

    @property
    def supports_direct_display(self) -> bool:
        """Indicates if this board supports external displays"""
        return self._supports_direct_display

    @supports_direct_display.setter
    def supports_direct_display(self, value):
        self._supports_direct_display = bool(value)

    @property
    def unique_id(self) -> Union[str, None]:
        """Unique identifier of the board or null if unknown"""
        return self._unique_id

    @unique_id.setter
    def unique_id(self, value):
        self._unique_id = str(value) if value is not None else None
