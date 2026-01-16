from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from pydantic.generics import GenericModel


# Create a Common Response Schema

T = TypeVar("T")


class APIResponse(GenericModel, Generic[T]):
    status: int
    message: str
    data: Optional[T]
