from ..model_object import ModelObject
from ..utils import model_prop


class StartupError(ModelObject):
    """
    Details about the first error on start-up
    """

    # Filename of the macro where the error occurred
    file = model_prop("file", str, "")

    # Line number of the error
    line = model_prop("line", int, 0)

    # Message of the error
    message = model_prop("message", str, "")

    def __init__(self):
        super().__init__()
