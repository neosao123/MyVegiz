
from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional, List
from datetime import datetime
import re


class ProductImageResponse(BaseModel):
    product_image: str
    is_primary: bool

    class Config:
        orm_from_attributes = True

        

class ProductResponse(BaseModel):
    uu_id: str
    category_id: int
    sub_category_id: Optional[int]   
    product_name: str
    product_short_name: str
    slug: str
    short_description: Optional[str]
    long_description: Optional[str]
    hsn_code: Optional[str]
    sku_code: Optional[str]
    is_active: bool
    created_at: datetime
    images: List[ProductImageResponse]

    class Config:
        orm_from_attributes = True