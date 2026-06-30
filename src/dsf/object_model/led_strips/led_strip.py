from enum import Enum

from .led_strip_color_order import LedStripColorOrder

from ..model_object import ModelObject
from ..utils import model_prop


class LedStripType(str, Enum):
    """Types of supported LED strips"""

    # DotStar LED strip
    DotStar = "DotStar"

    # NeoPixel LED strip with only RGB capability
    NeoPixel_RGB = "NeoPixel_RGB"

    # NeoPixel RGB LED strip with additional white output
    NeoPixel_RGBW = "NeoPixel_RGBW"


class LedStrip(ModelObject):
    """Type of this LED strip"""

    # Board address of the corresponding pin
    board = model_prop('board', int, 0)

    # Order in which colour components are sent to the strip
    color_order = model_prop('color_order', LedStripColorOrder, LedStripColorOrder.BGR)

    # Maximum number of LEDs that can be addressed on this strip
    max_leds = model_prop('max_leds', int, 0)

    # Name of the pin this LED strip is connected to
    pin = model_prop('pin', str, "")

    # Indicates if this strip is bit-banged and therefore requires motion to be stopped before sending a command
    stop_movement = model_prop('stop_movement', bool, False)

    # Type of this LED strip
    type = model_prop('type', LedStripType, LedStripType.DotStar)

    def __init__(self):
        super().__init__()
