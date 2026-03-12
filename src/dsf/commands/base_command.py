class BaseCommand:
    """Base class of a command."""

    @classmethod
    def from_json(cls, data: dict[str, object]) -> "BaseCommand":
        """Deserialize an instance of this class from a JSON deserialized dictionary"""
        command = data.get("command", "")
        kwargs = {key: value for key, value in data.items() if key != "command"}
        return cls(command=str(command), **kwargs)

    def __init__(self, command: str, **kwargs: object) -> None:
        self.command = command
        for key, value in kwargs.items():
            self.__dict__[key] = value
