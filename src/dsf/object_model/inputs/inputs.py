from typing import List, Optional

from .input_channel import InputChannel
from ..model_collection import ModelCollection
from ...commands.code_channel import CodeChannel


class Inputs(ModelCollection[Optional[InputChannel]]):

    def __init__(self):
        self._valid_channels = [CodeChannel(c) for c in CodeChannel if c is not CodeChannel.Unknown]
        # Like DSF, start with one input channel per code channel
        super().__init__(Optional[InputChannel], [self._create_channel(channel) for channel in self._valid_channels])

    @staticmethod
    def _create_channel(name: CodeChannel) -> InputChannel:
        return InputChannel.from_json({"name": name.value})

    @property
    def valid_channels(self) -> List[CodeChannel]:
        """List of valid channels"""
        return self._valid_channels

    @property
    def total(self) -> int:
        """Total number of supported input channel"""
        return len(self._valid_channels)
