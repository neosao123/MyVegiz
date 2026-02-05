from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime



# -------------------------
# SINGLE VARIANT ITEM
# Used inside bulk create payload
# -------------------------
class VariantItem(BaseModel):
    zone_id: int
    uom_id: int
    actual_price: float
    selling_price: float
    is_deliverable: Optional[bool] = True


# -------------------------
# BULK CREATE PAYLOAD
# Used to create multiple variants for one product
# -------------------------
class ProductVariantBulkCreate(BaseModel):
    product_id: int
    variants: List[VariantItem]


# -------------------------
# RESPONSE SCHEMA
# Used when returning variant details
# -------------------------

class ProductVariantResponse(BaseModel):
    id: int
    uu_id: str

    product_id: int
    product_name: str | None = None

    zone_id: int
    zone_name: str | None = None

    uom_id: int
    uom_name: str | None = None

    actual_price: float
    selling_price: float
    is_deliverable: bool
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True


# -------------------------
# ZONE DROPDOWN RESPONSE
# Used for UI dropdowns
# -------------------------
class ZoneDropdownResponse(BaseModel):
    zone_id: int
    zone_name: str

    class Config:
        orm_from_attributes = True

# -------------------------
# UOM DROPDOWN RESPONSE
# ------------------------
class UOMDropdownResponse(BaseModel):
    uom_id: int
    uom_name: str

    class Config:
        orm_from_attributes = True


# -------------------------
# PRODUCT DROPDOWN RESPONSE
# -------------------------
class ProductDropdownResponse(BaseModel):
    product_id: int
    product_name: str

    class Config:
        orm_from_attributes = True

