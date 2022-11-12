class IncompatibleVersionException(Exception):
    """Exception raised if the API version of the client is incompatible to the server"""


class InternalServerException(Exception):
    """Exception returned by the server for an arbitrary problem"""

    def __init__(self, command, error_type: str, error_message: str):
        super().__init__("Internal Server Exception")
        self.command = command
        self.error_type = error_type
        self.error_message = error_message


class TaskCanceledException(Exception):
    """Exception returned by the server if the task has been cancelled remotely"""
