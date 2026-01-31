from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime



# -------------------------
# RESPONSE SCHEMA
# -------------------------
class ProductVariantResponse(BaseModel):
    id: int
    uu_id: str
    product_id: int
    zone_id: int
    uom_id: int
    actual_price: float
    selling_price: float
    is_deliverable : bool
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True
