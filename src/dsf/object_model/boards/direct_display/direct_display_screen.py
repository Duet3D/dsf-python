from .direct_display_controller import DirectDisplayController
from ...model_object import ModelObject
from ...utils import model_prop
from ....utils import JSONElement


class DirectDisplayScreen(ModelObject):
    """Class providing information about a connected display screen"""

    # Number of colour bits
    colour_bits = model_prop("colour_bits",int, 1)
    
    # Display type
    controller = model_prop("controller", DirectDisplayController, DirectDisplayController.ST7920)
    
    # Height of the display screen in pixels
    height = model_prop("height",int, 64)
    
    # SPI frequency of the display (in Hz)
    spi_freq = model_prop("spi_freq",int, 0)
    
    # Width of the display screen in pixels
    width = model_prop("width",int, 128)
    
    def __init__(self, controller: DirectDisplayController = DirectDisplayController.ST7920):
        super().__init__()

        self.controller = controller

    @staticmethod
    def get_direct_display_screen_type(type_: DirectDisplayController):
        from .direct_display_screen_st7567 import DirectDisplayScreenST7567

        if type_ == DirectDisplayController.ST7920:
            return DirectDisplayScreen()
        elif type_ == DirectDisplayController.ST7567:
            return DirectDisplayScreenST7567()
        elif type_ == DirectDisplayController.ILI9488:
            return DirectDisplayScreen()
        else:
            return DirectDisplayScreen(type_)

    def _update_from_json(self, **kwargs: JSONElement):
        """Override ObjectModel._update_from_json
        to return the DirectDisplayScreen type matching the given controller"""
        if 'controller' in kwargs:
            controller = DirectDisplayController(kwargs.get('controller'))
            if controller != self.controller:
                required_type = self.get_direct_display_screen_type(controller)
                new_direct_display_screen = required_type.update_from_json(kwargs)
                return new_direct_display_screen

        super(DirectDisplayScreen, self)._update_from_json(**kwargs)
        return self
