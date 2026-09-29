import re

from typing import Optional, Self

from ..model_object import ModelObject
from ...exceptions import CodeParserException
from ...utils import JSONObj


def is_driverId(value: object) -> bool:
    return isinstance(value, DriverId)


class DriverId(ModelObject):
    """
    Class representing a driver identifier
    :param board: Board of this driver identifier
    :param port: Port of this driver identifier
    """

    board: int
    port: int

    def __init__(
        self,
        as_str: Optional[str] = None,
        as_int: Optional[int] = None,
        board: Optional[int] = None,
        port: Optional[int] = None,
    ):
        super().__init__()

        self.board = board if board is not None else 0
        self.port = port if port is not None else 0

        if as_int is not None:
            if as_int < 0:
                raise Exception("DriverId as int must not be negative")
            self.board = (as_int >> 16) & 0xFFFF
            self.port = as_int & 0xFFFF
            return

        if as_str is not None:
            segments = as_str.split(".")
            segment_count = len(segments)
            if segment_count == 1:
                self.board = 0
                self.port = int(segments[0])
            elif segment_count == 2:
                self.board = int(segments[0]) & 0xFFFF
                self.port = int(segments[1]) & 0xFFFF
            else:
                raise CodeParserException("Failed to parse driver value")
            return

    def as_int(self) -> int:
        return (self.board << 16) | self.port

    def __str__(self, **kwargs: object):
        """Convert this instance to a string"""
        return f"{self.board}.{self.port}"

    def __eq__(self, o: object) -> bool:
        """Checks whether this instance is equal to another"""
        return isinstance(o, DriverId) and self.board == o.board and self.port == o.port

    def __ne__(self, o: object) -> bool:
        return not self == o

    def __hash__(self) -> int:
        return hash((self.board, self.port))

    def update_from_json(self, data: JSONObj | str) -> Self:
        if not isinstance(data, str):
            raise TypeError(f"DriverId must be updated from a string. Got {type(data).__name__}: {data}")
        matches = re.search(r"(\d+)\.(\d+)", data)
        if matches:
            self.board = int(matches.group(1))
            self.port = int(matches.group(2))
        else:
            self.board = 0
            self.port = int(data)
        return self
