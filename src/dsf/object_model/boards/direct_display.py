from ..model_object import ModelObject


class DirectDisplay(ModelObject):
    """Class providing information about a connected display"""
    def __init__(self):
        super(DirectDisplay, self).__init__()
        # Number of pulses per click of the rotary encoder
        self._pulses_per_click = 0
        # SPI frequency of the display (in Hz)
        self._spi_freq = 0
        # Name of the attached display type
        self._type_name = ""

    @property
    def pulses_per_click(self) -> int:
        """Number of pulses per click of the rotary encoder"""
        return self._pulses_per_click

    @pulses_per_click.setter
    def pulses_per_click(self, value: int):
        self._pulses_per_click = int(value) if value is not None else 0

    @property
    def spi_freq(self) -> int:
        """SPI frequency of the display (in Hz)"""
        return self._spi_freq

    @spi_freq.setter
    def spi_freq(self, value: int):
        self._spi_freq = int(value) if value is not None else 0

    @property
    def type_name(self) -> str:
        """Name of the attached display type"""
        return self._type_name

    @type_name.setter
    def type_name(self, value: str):
        self._type_name = str(value)
