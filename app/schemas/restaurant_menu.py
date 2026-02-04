from pydantic import BaseModel
from fastapi import Form
from typing import Optional
from datetime import datetime


# -------------------------
# CREATE
# -------------------------
class MenuCreate(BaseModel):
    menu: str
    priority: Optional[int] = 0
    is_active: Optional[bool] = True

    @classmethod
    def as_form(
        cls,
        menu: str = Form(...),
        priority: int = Form(0),
        is_active: bool = Form(True),
    ):
        return cls(
            menu=menu.strip(),
            priority=priority,
            is_active=is_active
        )


# -------------------------
# RESPONSE
# -------------------------
class MenuResponse(BaseModel):
    id: int
    uu_id: str
    code: str
    menu: str
    priority: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True


# -------------------------
# UPDATE
# -------------------------
class MenuUpdate(BaseModel):
    menu: Optional[str] = None
    priority: Optional[int] = None
    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        menu: Optional[str] = Form(None),
        priority: Optional[int] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            menu=menu.strip() if menu else None,
            priority=priority,
            is_active=is_active
        )
