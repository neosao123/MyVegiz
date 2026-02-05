from pydantic import BaseModel, field_validator
from fastapi import Form
from datetime import datetime
from typing import Optional


# =====================================================
# Slider RESPONSE (WEB)
# =====================================================
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

