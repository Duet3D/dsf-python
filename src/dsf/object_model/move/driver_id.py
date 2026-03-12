import re

from ..model_object import ModelObject
from ...exceptions import CodeParserException


def is_driverId(value: object) -> bool:
    return isinstance(value, DriverId)


class DriverId(ModelObject):
    """
    Class representing a driver identifier
    :param board: Board of this driver identifier
    :param port: Port of this driver identifier
    """

    def __init__(
        self,
        as_str: str | None = None,
        as_int: int | None = None,
        board: int | None = None,
        port: int | None = None,
    ) -> None:
        super().__init__()
        self.board: int | None = None
        self.port: int = 0

        if board is not None:
            self.board = board
        if port is not None:
            self.port = port

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

    def as_int(self) -> int:
        board = 0 if self.board is None else self.board
        return (board << 16) | self.port

    def __str__(self, **kwargs: object) -> str:
        """Convert this instance to a string"""
        return f"{self.port}" if self.board is None else f"{self.board}.{self.port}"

    def __eq__(self, o: object) -> bool:
        """Checks whether this instance is equal to another"""
        return isinstance(o, DriverId) and self.board == o.board and self.port == o.port

    def __ne__(self, o: object) -> bool:
        return not self == o

    def update_from_json(self, data: dict[str, object] | str) -> "DriverId":
        if isinstance(data, str):
            matches = re.search(r'(\d+)\.(\d+)', data)
            if matches:
                self.board = int(matches.group(1))
                self.port = int(matches.group(2))
            else:
                self.board = None
                self.port = int(data)
        elif isinstance(data, dict):
            super().update_from_json(data)
        return self

