from typing import List, Optional

from .input_channel import InputChannel
from ..model_collection import ModelCollection
from ...commands.code_channel import CodeChannel


class Inputs(ModelCollection[Optional[InputChannel]]):

    def __init__(self):
        super().__init__(Optional[InputChannel])
        self._valid_channels = [CodeChannel(c) for c in CodeChannel if c is not CodeChannel.Unknown]

    @property
    def valid_channels(self) -> List[CodeChannel]:
        """List of valid channels"""
        return self._valid_channels

    @property
    def total(self) -> int:
        """Total number of supported input channel"""
        return len(self._valid_channels)
