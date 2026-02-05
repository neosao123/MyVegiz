from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional
from datetime import datetime

# =========================================================
# SUB CATEGORY CREATE SCHEMA
# Used to create a new sub-category under a category
# =========================================================
class SubCategoryCreate(BaseModel):
    category_id: int
    sub_category_name: str
    is_active: bool = True

    # -----------------------------------------------------
    # FORM SUPPORT
    # Enables multipart/form-data submission
    # -----------------------------------------------------
    @classmethod
    def as_form(
        cls,
        category_id: int = Form(...),
        sub_category_name: str = Form(...),
        is_active: bool = Form(True),
    ):
        return cls(
            category_id=category_id,
            sub_category_name=sub_category_name.strip(),
            is_active=is_active,
        )

    @field_validator("sub_category_name")
    @classmethod
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError("Sub category name must be at least 3 characters")
        return v

# =========================================================
# SUB CATEGORY UPDATE SCHEMA
# Used to update an existing sub-category
# All fields are optional
# =========================================================
class SubCategoryUpdate(BaseModel):
    category_id: Optional[int] = None
    sub_category_name: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        category_id: Optional[int] = Form(None),
        sub_category_name: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            category_id=category_id,
            sub_category_name=sub_category_name.strip() if sub_category_name else None,
            is_active=is_active,
        )


# =========================================================
# SUB CATEGORY RESPONSE SCHEMA
# Used when returning sub-category data in API responses
# =========================================================
class SubCategoryResponse(BaseModel):
    id: int
    uu_id: str
    category_id: int
    category_name:Optional[str]=None
    sub_category_name: str
    slug: str
    sub_category_image: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True


# =========================================================
# CATEGORY DROPDOWN RESPONSE
# Used for dropdowns (ID + Name only)
# =========================================================
class CategoryDropdownResponse(BaseModel):
    id: int
    category_name: str

    class Config:
        orm_from_attributes = True

