from .direct_display_encoder import DirectDisplayEncoder
from .direct_display_screen import DirectDisplayScreen

from ...model_object import ModelObject
from ...utils import nullable_model_prop, model_prop


class DirectDisplay(ModelObject):
    """Class providing information about a connected direct-connect display"""

    # Encoder of this screen or null if none
    encoder = nullable_model_prop('encoder', DirectDisplayEncoder)
    
    # Screen information
    screen = model_prop('screen', DirectDisplayScreen, DirectDisplayScreen())

    def __init__(self):
        super(DirectDisplay, self).__init__()
