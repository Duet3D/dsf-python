from typing import List

from .input_channel import InputChannel
from ..model_collection import ModelCollection
from ...commands.code_channel import CodeChannel


class Inputs(ModelCollection):

    def __init__(self):
        super().__init__(InputChannel)
        self._valid_channels = [CodeChannel(c) for c in CodeChannel if c is not CodeChannel.Unknown]

    @property
    def valid_channels(self) -> List[CodeChannel]:
        """Enumeration of valid code channels"""
        return self._valid_channels

    @property
    def total(self) -> int:
        """Total number of supported input channel"""
        return len(self._valid_channels)
