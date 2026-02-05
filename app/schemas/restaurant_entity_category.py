# app/schemas/restaurant_entity_category.py
from pydantic import BaseModel
from fastapi import Form
from typing import Optional
from datetime import datetime

# =====================================================
# ENTITY CATEGORY – CREATE SCHEMA
# Used when creating a new entity category
# =====================================================
class EntityCategoryCreate(BaseModel):
    entity_category: str
    main_category_id: Optional[int] = 17
    is_active: bool = True

    @classmethod
    def as_form(
        cls,
        entity_category: str = Form(...),
        main_category_id: int = Form(17),
        is_active: bool = Form(True),
    ):
        return cls(
            entity_category=entity_category.strip(),
            main_category_id=main_category_id,
            is_active=is_active
        )



# =====================================================
# ENTITY CATEGORY – RESPONSE SCHEMA
# Used for API responses (list / create / update)
# =====================================================
class EntityCategoryResponse(BaseModel):
    id: int
    uu_id: str
    code: str
    entity_category: str
    main_category_id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True



# =====================================================
# ENTITY CATEGORY – UPDATE SCHEMA
# Used when updating an existing entity category
# =====================================================
class EntityCategoryUpdate(BaseModel):
    entity_category: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        entity_category: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            entity_category=entity_category.strip() if entity_category else None,
            is_active=is_active
        )