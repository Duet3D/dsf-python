from enum import Enum

class LedStripColorOrder(int, Enum):
    """Color order of the LED strip"""

    # Default order for DotStar LEDs
    BGR = 0,

    # Blue, red, green
    BRG = 1,

    # Red, green, blue
    RGB = 2,

    # Red, blue, green
    RBG = 3,

    # Green, blue, red
    GBR = 4,

    # Default order for WS2812 (NeoPixel) LEDs
    GRB = 5