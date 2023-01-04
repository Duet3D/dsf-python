from ..model_object import ModelObject


class BeepRequest(ModelObject):
    """Details about a requested beep"""
    def __init__(self):
        super(BeepRequest, self).__init__()
        self._duration = 0
        self._frequency = 0

    @property
    def duration(self) -> int:
        """Duration of the requested beep (in ms)"""
        return self._duration

    @duration.setter
    def duration(self, value: int):
        self._duration = int(value)

    @property
    def frequency(self) -> int:
        """Frequency of the requested beep (in Hz)"""
        return self._frequency

    @frequency.setter
    def frequency(self, value: int):
        self._frequency = int(value)
