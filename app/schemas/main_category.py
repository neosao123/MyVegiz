# app/schemas/main_category.py
from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional
from datetime import datetime

# -------------------------
# CREATE MAIN CATEGORY
# -------------------------
class MainCategoryCreate(BaseModel):
    main_category_name: str
    is_active: bool = True

    # -------------------------
    # FORM SUPPORT
    # Enables multipart/form-data submission
    # -------------------------
    @classmethod
    def as_form(
        cls,
        main_category_name: str = Form(...),
        is_active: bool = Form(True),
    ):
        return cls(
            main_category_name=main_category_name.strip(),
            is_active=is_active,
        )

    @field_validator("main_category_name")
    @classmethod
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError("Main category name must be at least 3 characters")
        return v

# -------------------------
# UPDATE MAIN CATEGORY
# -------------------------
class MainCategoryUpdate(BaseModel):
    main_category_name: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        main_category_name: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            main_category_name=main_category_name.strip() if main_category_name else None,
            is_active=is_active,
        )



# -------------------------
# MAIN CATEGORY RESPONSE
# -------------------------
class MainCategoryResponse(BaseModel):
    id: int
    uu_id: str
    main_category_name: str
    slug: str
    main_category_image: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True
