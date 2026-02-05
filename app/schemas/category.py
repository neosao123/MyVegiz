from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional
from datetime import datetime
import re

# -------------------------
# CATEGORY CREATE SCHEMA
# -------------------------
class CategoryCreate(BaseModel):
    main_category_id: int
    category_name: str
    is_active: bool = True

    @classmethod
    def as_form(
        cls,
        main_category_id: int = Form(...),
        category_name: str = Form(...),
        is_active: bool = Form(True),
    ):
        return cls(
            main_category_id=main_category_id,
            category_name=category_name,
            is_active=is_active,
        )

    # ---------- REQUIRED ----------
    @field_validator("category_name", mode="before")
    @classmethod
    def required_category_name(cls, v):
        if v is None or not v.strip():
            raise ValueError("Category name is required")
        return v.strip()

    # ---------- FORMAT ----------
    @field_validator("category_name")
    @classmethod
    def validate_category_name(cls, v):
        if len(v) < 3:
            raise ValueError("Category name must be at least 3 characters long")
        return v


# -------------------------
# CATEGORY RESPONSE SCHEMA
# -------------------------
class CategoryResponse(BaseModel):
    id: int
    main_category_id: Optional[int] = None
    main_category_name:Optional[str]=None
    uu_id: str
    category_name: str
    slug: str
    category_image: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True


# -------------------------
# CATEGORY UPDATE SCHEMA
# -------------------------
class CategoryUpdate(BaseModel):
    main_category_id: Optional[int] = None
    category_name: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        main_category_id: Optional[int] = Form(None),
        category_name: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            main_category_id=main_category_id,
            category_name=category_name.strip() if category_name else None,
            is_active=is_active,
        )

    # ---------- VALIDATION ----------
    @field_validator("category_name")
    @classmethod
    def validate_category_name(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError("Category name is required")
            if len(v) < 3:
                raise ValueError("Category name must be at least 3 characters long")
        return v

# -------------------------
# MAIN CATEGORY DROPDOWN RESPONSE
# -------------------------
class MainCategoryDropdownResponse(BaseModel):
    id: int
    main_category_name: str

    class Config:
        orm_from_attributes = True


