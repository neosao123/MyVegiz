from typing import Generic, TypeVar, Optional,Dict,Any
from pydantic import BaseModel
from pydantic.generics import GenericModel


# Create a Common Response Schema

T = TypeVar("T")


class APIResponse(GenericModel, Generic[T]):
    status: int
    message: str
    data: Optional[T]


class PaginatedAPIResponse(GenericModel, Generic[T]):
    status: int
    message: str
    data: Optional[T]
    pagination: Dict[str, Any]  
