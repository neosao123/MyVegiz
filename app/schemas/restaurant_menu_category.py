from pydantic import BaseModel
from fastapi import Form
from typing import Optional
from datetime import datetime


class MenuCategoryCreate(BaseModel):
    menu_id: int
    menu_category: str
    is_active: bool = True

    @classmethod
    def as_form(
        cls,
        menu_id: int = Form(...),
        menu_category: str = Form(...),
        is_active: bool = Form(True),
    ):
        return cls(
            menu_id=menu_id,
            menu_category=menu_category.strip(),
            is_active=is_active
        )


class MenuCategoryResponse(BaseModel):
    id: int
    uu_id: str
    code: str
    menu_id: int
    menu_category: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True


class MenuCategoryUpdate(BaseModel):
    menu_category: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        menu_category: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            menu_category=menu_category.strip() if menu_category else None,
            is_active=is_active
        )


class MenuDropdownResponse(BaseModel):
    menu_id: int
    menu_name: str

    class Config:
        orm_from_attributes = True