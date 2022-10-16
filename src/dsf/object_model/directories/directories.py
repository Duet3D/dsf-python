from ..model_object import ModelObject


class Directories(ModelObject):
    """Information about the configured directories"""
    def __init__(self):
        super().__init__()
        # Path to the filaments directory
        self._filaments = "0:/filaments"
        # Path to the firmware directory
        self._firmware = "0:/firmware"
        # Path to the G-Codes directory
        self._g_codes = "0:/gcodes"
        # Path to the macros directory
        self._macros = "0:/macros"
        # Path to the menu directory
        # Intended for 12864 displays but currently unused in DSF. It is only needed for the Duet Maestro > DWC
        self._menu = "0:/menu"
        # Path to the scans directory
        self._scans = "0:/scans"
        # Path to the system directory
        self._system = "0:/sys"
        # Path to the web directory
        self._web = "0:/www"

    @property
    def filaments(self) -> str:
        """Path to the filaments directory"""
        return self._filaments

    @filaments.setter
    def filaments(self, value):
        self._filaments = str(value)

    @property
    def firmware(self) -> str:
        """Path to the firmware directory"""
        return self._firmware

    @firmware.setter
    def firmware(self, value):
        self._firmware = str(value)

    @property
    def g_codes(self) -> str:
        """Path to the G-Codes directory"""
        return self._g_codes

    @g_codes.setter
    def g_codes(self, value):
        self._g_codes = str(value)

    @property
    def macros(self) -> str:
        """Path to the macros directory"""
        return self._macros

    @macros.setter
    def macros(self, value):
        self._macros = str(value)

    @property
    def menu(self) -> str:
        """Path to the menu directory
        Intended for 12864 displays but currently unused in DSF. It is only needed for the Duet Maestro > DWC"""
        return self._menu

    @menu.setter
    def menu(self, value):
        self._menu = str(value)

    @property
    def scans(self) -> str:
        """Path to the scans directory"""
        return self._scans

    @scans.setter
    def scans(self, value):
        self._scans = str(value)

    @property
    def system(self) -> str:
        """Path to the system directory"""
        return self._system

    @system.setter
    def system(self, value):
        self._system = str(value)

    @property
    def web(self) -> str:
        """Path to the web directory"""
        return self._web

    @web.setter
    def web(self, value):
        self._web = str(value)
