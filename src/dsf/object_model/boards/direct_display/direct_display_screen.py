from .direct_display_controller import DirectDisplayController
from ...model_object import ModelObject
from ...utils import model_prop
from ....utils import JSONElement


class DirectDisplayScreen(ModelObject):
    """Class providing information about a connected display screen"""

    # Number of colour bits
    colour_bits = model_prop("colour_bits", int, 1)

    # Display type
    controller = model_prop("controller", DirectDisplayController, DirectDisplayController.ST7920)

    # Height of the display screen in pixels
    height = model_prop("height", int, 64)

    # SPI frequency of the display (in Hz)
    spi_freq = model_prop("spi_freq", int, 0)

    # Width of the display screen in pixels
    width = model_prop("width", int, 128)

    def __init__(self, controller: DirectDisplayController = DirectDisplayController.ST7920):
        super().__init__()

        self.controller = controller

    @staticmethod
    def get_direct_display_screen_type(type_: DirectDisplayController):
        from .direct_display_screen_st7567 import DirectDisplayScreenST7567

        if type_ == DirectDisplayController.ST7567:
            return DirectDisplayScreenST7567()
        return DirectDisplayScreen(type_)

    def _update_from_json(self, **kwargs: JSONElement):
        """Override ObjectModel._update_from_json
        to return the DirectDisplayScreen type matching the given controller"""
        if "controller" in kwargs:
            required_type = self.get_direct_display_screen_type(DirectDisplayController(kwargs.get("controller")))
            # Like DSF, only replace this screen if the controller needs a different class,
            # e.g. switching from ST7920 to ILI9488 updates this screen
            if type(required_type) is not type(self):
                return required_type.update_from_json(kwargs)

        super(DirectDisplayScreen, self)._update_from_json(**kwargs)
        return self
