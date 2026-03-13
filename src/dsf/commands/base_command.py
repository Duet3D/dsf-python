from typing import Any

class BaseCommand:
    """Base class of a command."""

    @classmethod
    def from_json(cls, data: Any):
        """Deserialize an instance of this class from a JSON deserialized dictionary"""
        return cls(**data)

    def __init__(self, command: str, **kwargs: Any):
        self.command = command
        for key, value in kwargs.items():
            self.__dict__[key] = value
