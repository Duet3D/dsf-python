from typing import Union

from .direct_display_controller import DirectDisplayController
from ...model_object import ModelObject


class DirectDisplayScreen(ModelObject):
    """Class providing information about a connected display screen"""

    def __init__(self, controller=DirectDisplayController.ST7920):
        super().__init__()
        # Number of colour bits
        self._colour_bits = 1
        # Display type
        self._controller = controller
        # Height of the display screen in pixels
        self._height = 64
        # SPI frequency of the display (in Hz)
        self._spi_freq = 0
        # Width of the display screen in pixels
        self._width = 128

    @property
    def colour_bits(self) -> int:
        """Number of colour bits"""
        return self._colour_bits

    @colour_bits.setter
    def colour_bits(self, value: int):
        self._colour_bits = int(value)

    @property
    def controller(self) -> DirectDisplayController:
        """Number of colour bits"""
        return self._controller

    @controller.setter
    def controller(self, value: Union[DirectDisplayController, str]):
        if isinstance(value, DirectDisplayController):
            self._controller = value
        elif isinstance(value, str):
            self._controller = DirectDisplayController(value.upper())
        else:
            raise TypeError(f"{__name__}.controller must be of type DirectDisplayController."
                            f"Got {type(value)}: {value}")

    @staticmethod
    def get_direct_display_screen_type(type_: DirectDisplayController):
        from .direct_display_screen_st7567 import DirectDisplayScreenST7567

        if isinstance(type_, str):
            type_ = DirectDisplayController(type_)
        elif not isinstance(type_, DirectDisplayController):
            raise TypeError(f"type must be of type DirectDisplayController. Got {type(type_)}: {type_}")

        if type_ == DirectDisplayController.ST7920:
            return DirectDisplayScreen()
        elif type_ == DirectDisplayController.ST7567:
            return DirectDisplayScreenST7567()
        elif type_ == DirectDisplayController.ILI9488:
            return DirectDisplayScreen()
        else:
            return DirectDisplayScreen(type_)

    @property
    def height(self) -> int:
        """Height of the display screen in pixels"""
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = int(value)

    @property
    def spi_freq(self) -> int:
        """SPI frequency of the display (in Hz)"""
        return self._spi_freq

    @spi_freq.setter
    def spi_freq(self, value: int):
        self._spi_freq = int(value)

    @property
    def width(self) -> int:
        """Width of the display screen in pixels"""
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = int(value)

    def _update_from_json(self, **kwargs):
        """Override ObjectModel._update_from_json
        to return the DirectDisplayScreen type matching the given controller"""
        if 'controller' in kwargs and self.controller != DirectDisplayController(kwargs.get('controller')):
            required_type = self.get_direct_display_screen_type(kwargs.get('controller'))
            new_direct_display_screen = required_type.update_from_json(kwargs)
            return new_direct_display_screen

        super(DirectDisplayScreen, self)._update_from_json(**kwargs)
        return self
