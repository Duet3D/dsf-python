from .direct_display_encoder import DirectDisplayEncoder
from .direct_display_screen import DirectDisplayScreen

from ...model_object import ModelObject
from ...utils import wrap_model_property


class DirectDisplay(ModelObject):
    """Class providing information about a connected direct-connect display"""

    encoder = wrap_model_property('encoder', DirectDisplayEncoder)

    def __init__(self):
        super(DirectDisplay, self).__init__()
        # Encoder of this screen or null if none
        self._encoder = None
        # Screen information
        self._screen = DirectDisplayScreen()

    @property
    def screen(self) -> DirectDisplayScreen:
        """Screen information"""
        return self._screen
