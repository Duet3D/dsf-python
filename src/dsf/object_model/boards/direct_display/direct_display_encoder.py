from ...model_object import ModelObject


class DirectDisplayEncoder(ModelObject):
    """Class providing information about a connected display encoder"""

    def __init__(self):
        super().__init__()
        # Number of pulses per click of the rotary encoder
        self._pulses_per_click = 1

    @property
    def pulses_per_click(self) -> int:
        """Number of pulses per click of the rotary encoder"""
        return self._pulses_per_click

    @pulses_per_click.setter
    def pulses_per_click(self, value: int):
        self._pulses_per_click = int(value)
