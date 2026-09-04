from typing import TypeVar, Type
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class JsonParser:

    @staticmethod
    def deserialize(
        value: str,
        model: Type[T],
    ) -> T:
        return model.model_validate_json(value)

    @staticmethod
    def serialize(
        value: BaseModel,
    ) -> str:
        return value.model_dump_json()
