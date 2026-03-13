from ...utils import model_prop

from .direct_display_screen import DirectDisplayScreen
from .direct_display_controller import DirectDisplayController


class DirectDisplayScreenST7567(DirectDisplayScreen):
    """Direct-connected display screen with a ST7567 controller"""

    contrast = model_prop("contrast", int, 30)
    resistor_ratio = model_prop("resistor_ratio", int, 6)

    def __init__(self):
        super().__init__(controller=DirectDisplayController.ST7567)
