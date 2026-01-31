from pydantic import BaseModel
from fastapi import Form
from typing import Optional
from datetime import datetime
import re



class CategoryResponse(BaseModel):
    id: int
    main_category_id: Optional[int] = None
    main_category_name: Optional[str] = None   
    uu_id: str
    category_name: str
    slug: str
    category_image: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True
