from typing import Self, TypeVar, Protocol, TypeAlias, runtime_checkable

from ..utils import JSONElement

T = TypeVar("T", bound=JSONElement)
TModelValue: TypeAlias = "ModelType[T]"

@runtime_checkable
class ModelType(Protocol[T]):
    @classmethod
    def from_json(cls: type[T], data: T) -> T:
        """Deserialize a new instance of this class from JSON deserialized dictionary"""
        ...

    def update_from_json(self, data: T) -> Self:
        """Update the current instance of this class from JSON deserialized dictionary"""
        ...

    def to_json(self) -> str:
        """Serialize this instance of this class into a JSON dictionary"""
        return self.__str__()
