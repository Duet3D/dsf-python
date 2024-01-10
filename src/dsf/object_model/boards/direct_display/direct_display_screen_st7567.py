from .direct_display_screen import DirectDisplayScreen
from .direct_display_controller import DirectDisplayController


class DirectDisplayScreenST7567(DirectDisplayScreen):
    """Direct-connected display screen with a ST7567 controller"""

    def __init__(self):
        super().__init__(controller=DirectDisplayController.ST7567)
        # Configured contrast
        self._contrast = 30
        # Configured resistor ratio
        self._resistor_ratio = 6

    @property
    def contrast(self) -> int:
        """Configured contrast"""
        return self._contrast

    @contrast.setter
    def contrast(self, value: int):
        self._contrast = int(value)

    @property
    def resistor_ratio(self) -> int:
        """Configured resistor ratio"""
        return self._resistor_ratio

    @resistor_ratio.setter
    def resistor_ratio(self, value: int):
        self._resistor_ratio = int(value)
