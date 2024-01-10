from enum import Enum


class DirectDisplayController(str, Enum):
    """Enumeration of possible direct-connect display controllers"""

    # ST7920 controller
    ST7920 = "ST7920"

    # ST7567 controller
    ST7567 = "ST7567"

    # ILI9488 controller
    ILI9488 = "ILI9488"
