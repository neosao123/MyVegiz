from pydantic import BaseModel
from datetime import datetime


class ProductMiniResponse(BaseModel):
    id: int
    product_name: str
    slug: str

    class Config:
        orm_from_attributes = True


class UOMMiniResponse(BaseModel):
    id: int
    uom_name: str
    uom_short_name: str

    class Config:
        orm_from_attributes = True


class ProductVariantResponse(BaseModel):
    id: int
    uu_id: str
    actual_price: float
    selling_price: float
    is_deliverable: bool
    is_active: bool
    created_at: datetime

    product: ProductMiniResponse
    uom: UOMMiniResponse

    class Config:
        orm_from_attributes = True
