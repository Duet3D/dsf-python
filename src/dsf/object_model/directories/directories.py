from ..model_object import ModelObject
from ..utils import model_prop


class Directories(ModelObject):
    """Information about the configured directories"""

    # Path to the filaments directory
    filaments = model_prop("filaments", str, "0:/filaments")

    # Path to the firmware directory
    firmware = model_prop("firmware", str, "0:/firmware")

    # Path to the G-Codes directory
    g_codes = model_prop("g_codes", str, "0:/gcodes")

    # Path to the macros directory
    macros = model_prop("macros", str, "0:/macros")

    # Path to the menu directory
    # Intended for 12864 displays but currently unused in DSF. It is only needed
    # for the Duet Maestro > DWC
    menu = model_prop("menu", str, "0:/menu")

    # Path to the system directory
    system = model_prop("system", str, "0:/sys")

    # Path to the web directory
    web = model_prop("web", str, "0:/www")

    def __init__(self):
        super().__init__()
