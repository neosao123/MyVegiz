from pydantic import BaseModel, field_validator
from fastapi import Form
from datetime import datetime
from typing import Optional

class SliderCreate(BaseModel):
    caption: str
    is_active: bool = True

    @classmethod
    def as_form(
        cls,
        caption: str = Form(...),
        is_active: bool = Form(True),
    ):
        return cls(
            caption=caption.strip(),
            is_active=is_active
        )

    @field_validator("caption")
    @classmethod
    def validate_caption(cls, v):
        if len(v) < 3:
            raise ValueError("Caption must be at least 3 characters long")
        return v


class SliderResponse(BaseModel):
    id: int
    mobile_image: str
    tab_image: str
    web_image: str
    caption: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True


class SliderUpdate(BaseModel):
    caption: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        caption: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            caption=caption.strip() if caption else None,
            is_active=is_active
        )

    @field_validator("caption")
    @classmethod
    def validate_caption(cls, v):
        if v and len(v) < 3:
            raise ValueError("Caption must be at least 3 characters long")
        return v
