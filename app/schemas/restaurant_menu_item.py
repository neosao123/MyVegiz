from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional
from datetime import datetime


# =====================================================
# MENU ITEM – CREATE SCHEMA
# Used when creating a new menu item
# =====================================================
class MenuItemCreate(BaseModel):
    item: str
    sale_price: float
    packing_charges: float
    max_order_quantity: int
    cuisine_type: str
    menu_id: int
    menu_category_id: Optional[int] = None

    description: Optional[str] = None
    item_status: Optional[str] = "available"
    is_approved: Optional[bool] = False
    is_active: bool = True

    @classmethod
    def as_form(
        cls,
        item: str = Form(...),
        sale_price: float = Form(...),
        packing_charges: float = Form(...),
        max_order_quantity: int = Form(...),
        cuisine_type: str = Form(...),
        menu_id: int = Form(...),
        menu_category_id: Optional[int] = Form(None),
        description: Optional[str] = Form(None),
        item_status: str = Form("available"),
        is_approved: bool = Form(False),
        is_active: bool = Form(True),
    ):
        return cls(
            item=item.strip(),
            sale_price=sale_price,
            packing_charges=packing_charges,
            max_order_quantity=max_order_quantity,
            cuisine_type=cuisine_type.strip(),
            menu_id=menu_id,
            menu_category_id=menu_category_id,
            description=description,
            item_status=item_status,
            is_approved=is_approved,
            is_active=is_active
        )

    # ---------- VALIDATION ----------
    @field_validator("item")
    @classmethod
    def validate_item(cls, v):
        if not v.strip():
            raise ValueError("Item name is required")
        return v

    @field_validator("sale_price")
    @classmethod
    def validate_sale_price(cls, v):
        if v <= 0:
            raise ValueError("Sale price must be greater than 0")
        return v

    @field_validator("max_order_quantity")
    @classmethod
    def validate_max_qty(cls, v):
        if v <= 0:
            raise ValueError("Maximum order quantity must be greater than 0")
        return v


# =====================================================
# MENU ITEM – UPDATE SCHEMA
# Used when updating an existing menu item
# =====================================================
class MenuItemUpdate(BaseModel):
    item: Optional[str] = None
    sale_price: Optional[float] = None
    packing_charges: Optional[float] = None
    max_order_quantity: Optional[int] = None
    cuisine_type: Optional[str] = None
    description: Optional[str] = None
    item_status: Optional[str] = None
    is_approved: Optional[bool] = None
    is_active: Optional[bool] = None
    menu_id: Optional[int] = None
    menu_category_id: Optional[int] = None

    @classmethod
    def as_form(
        cls,
        item: Optional[str] = Form(None),
        sale_price: Optional[float] = Form(None),
        packing_charges: Optional[float] = Form(None),
        max_order_quantity: Optional[int] = Form(None),
        cuisine_type: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        item_status: Optional[str] = Form(None),
        is_approved: Optional[bool] = Form(None),
        is_active: Optional[bool] = Form(None),
        menu_id: Optional[int] = Form(None),
        menu_category_id: Optional[int] = Form(None),
    ):
        return cls(
            item=item.strip() if item else None,
            sale_price=sale_price,
            packing_charges=packing_charges,
            max_order_quantity=max_order_quantity,
            cuisine_type=cuisine_type.strip() if cuisine_type else None,
            description=description,
            item_status=item_status,
            is_approved=is_approved,
            is_active=is_active,
            menu_id=menu_id,
            menu_category_id=menu_category_id,
        )


# =====================================================
# MENU ITEM – RESPONSE SCHEMA
# Used for API responses (create / list / update)
# =====================================================
class MenuItemResponse(BaseModel):
    id: int
    uu_id: str
    code: str
    item: str
    sale_price: float
    packing_charges: float
    max_order_quantity: int
    cuisine_type: str
    menu_id: int
    menu_category_id: Optional[int]
    description: Optional[str]
    item_image: Optional[str]
    item_status: str
    is_approved: bool
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True



# =====================================================
# MENU DROPDOWN RESPONSE
# Used for menu dropdown (id + menu name)
# =====================================================
class MenuDropdownResponse(BaseModel):
    id: int
    menu: str

    class Config:
        orm_from_attributes = True


# =====================================================
# MENU CATEGORY DROPDOWN RESPONSE
# Used for menu category dropdown by menu_id
# =====================================================
class MenuCategoryDropdownResponse(BaseModel):
    id: int
    menu_category: str

    class Config:
        orm_from_attributes = True
