from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# =====================================================
# PRODUCT IMAGE 
# =====================================================
class ProductImageMiniResponse(BaseModel):
    product_image: str

    class Config:
        orm_from_attributes = True


# =====================================================
# CATEGORY 
# =====================================================
class CategoryMiniResponse(BaseModel):
    id: int
    category_name: str

    class Config:
        orm_from_attributes = True


# =====================================================
# SUB-CATEGORY 
# =====================================================
class SubCategoryMiniResponse(BaseModel):
    id: int
    sub_category_name: str

    class Config:
        orm_from_attributes = True


# =====================================================
# PRODUCT 
# =====================================================
class ProductMiniResponse(BaseModel):
    id: int
    product_name: str
    slug: str

    product_image: Optional[str] = None  # SINGLE IMAGE

    category: CategoryMiniResponse
    sub_category: Optional[SubCategoryMiniResponse] = None

    class Config:
        orm_from_attributes = True

    @staticmethod
    def get_primary_image(obj):
        if not obj.images:
            return None
        for img in obj.images:
            if img.is_primary and not img.is_delete and img.is_active:
                return img.product_image
        return None


# =====================================================
# UNIT OF MEASUREMENT 
# =====================================================
class UOMMiniResponse(BaseModel):
    id: int
    uom_name: str
    uom_short_name: str

    class Config:
        orm_from_attributes = True


# =====================================================
# PRODUCT VARIANT RESPONSE
# =====================================================
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
