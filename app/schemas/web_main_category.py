from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WebMainCategoryResponse(BaseModel):
    id: int
    uu_id: str
    main_category_name: str
    slug: str
    main_category_image: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True
