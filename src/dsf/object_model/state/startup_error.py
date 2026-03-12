from ..model_object import ModelObject


class StartupError(ModelObject):
    """
    Details about the first error on start-up
    """

    def __init__(self) -> None:
        super().__init__()

        # Filename of the macro where the error occurred
        self._file: str = ""
        # Line number of the error
        self._line: int = 0
        # Message of the error
        self._message: str = ""

    @property
    def file(self) -> str:
        """Filename of the macro where the error occurred"""
        return self._file

    @file.setter
    def file(self, value: str):
        self._file = str(value)

    @property
    def line(self) -> int:
        """Line number of the error"""
        return self._line

    @line.setter
    def line(self, value: int | str):
        self._line = int(value)

    @property
    def message(self) -> str:
        """Message of the error"""
        return self._message

    @message.setter
    def message(self, value: str):
        self._message = str(value)
