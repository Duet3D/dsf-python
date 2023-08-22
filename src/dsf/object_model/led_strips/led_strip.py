from enum import Enum
from typing import Union

from ..model_object import ModelObject


class LedStripType(str, Enum):
    """Types of supported LED strips"""

    # DotStar LED strip
    DotStar = "dotstar"

    # NeoPixel LED strip with only RGB capability
    NeoPixel_RGB = "neopixel_rgb"

    # NeoPixel RGB LED strip with additional white output
    NeoPixel_RGBW = "neopixel_rgbw"


class LedStrip(ModelObject):
    """Type of this LED strip"""

    def __init__(self):
        super().__init__()
        # Board address of the corresponding pin
        self._board = 0
        # Name of the pin this LED strip is connected to
        self._pin = ""
        # Indicates if this strip is bit-banged and therefore requires motion to be stopped before sending a command
        self._stop_movement = False
        # Type of this LED strip
        self._type = LedStripType.DotStar

    @property
    def board(self) -> int:
        """Board address of the corresponding pin"""
        return self._board

    @board.setter
    def board(self, value: int):
        self._board = int(value)

    @property
    def pin(self) -> str:
        """Name of the pin this LED strip is connected to"""
        return self._pin

    @pin.setter
    def pin(self, value: str):
        self._pin = str(value)

    @property
    def stop_movement(self) -> bool:
        """Indicates if this strip is bit-banged and therefore requires motion to be stopped before sending a command"""
        return self._stop_movement

    @stop_movement.setter
    def stop_movement(self, value: bool):
        self._stop_movement = bool(value)

    @property
    def type(self) -> LedStripType:
        """Type of this LED strip"""
        return self._type

    @type.setter
    def type(self, value: Union[str, LedStripType] = LedStripType.DotStar):
        if isinstance(value, LedStripType):
            self._type = value
        elif isinstance(value, str):
            self._type = LedStripType(value.lower())
        else:
            raise TypeError(f"{__name__}.type must be of type LedStripType."
                            f"Got {type(value)}: {value}")
