from pydantic import BaseModel, field_validator
from fastapi import Form
from datetime import datetime


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
