from pydantic import BaseModel
from datetime import datetime
from typing import Optional





class CategoryMiniResponse(BaseModel):
    id: int
    category_name: str

    class Config:
        orm_from_attributes = True



class SubCategoryMiniResponse(BaseModel):
    id: int
    sub_category_name: str

    class Config:
        orm_from_attributes = True


class ProductMiniResponse(BaseModel):
    id: int
    product_name: str
    slug: str

    category: CategoryMiniResponse
    sub_category: Optional[SubCategoryMiniResponse] = None  #  OPTIONAL

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
