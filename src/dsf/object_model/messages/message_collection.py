from typing import List, Optional

from .messages import Message
from ..model_collection import ModelCollection
from ...utils import JSONElement


class MessageCollection(ModelCollection[Message]):
    """
    List of generic messages.
    Like in DSF, updating it from JSON adds the given messages instead of replacing the existing ones,
    because DSF clears its messages once they have been sent so every object model patch only holds new messages.
    Clear this list once the messages have been processed.
    """

    def __init__(self, value: Optional[List[Message]] = None):
        super().__init__(Message, value)

    def update_from_json(self, data: list[JSONElement]) -> "MessageCollection":
        # Nested JSON can reach this without type checking, so validate at runtime
        if not isinstance(data, list):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise Exception(f"Invalid JSON element type for message collection {type(data)}.")

        self.extend(ModelCollection(Message, data))
        return self
