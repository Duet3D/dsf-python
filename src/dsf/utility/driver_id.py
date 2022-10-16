from ..exceptions import CodeParserException


class DriverId:
    """
    Class representing a driver identifier
    :param board: Board of this driver identifier
    :param port: Port of this driver identifier
    """

    def __init__(self, as_str: str = None, as_int: int = None, board: int = None, port: int = None):
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

    def as_int(self):
        return (self.board << 16) | self.port

    def __str__(self):
        """Convert this instance to a string"""
        return f"{self.port}" if self.board is None else f"{self.board}.{self.port}"

    def __eq__(self, o):
        """Checks whether this instance is equal to another"""
        if self is None:
            return o is None
        return isinstance(o, DriverId) and self.board == o.board and self.port == o.port

    def __ne__(self, o):
        return not self == o
