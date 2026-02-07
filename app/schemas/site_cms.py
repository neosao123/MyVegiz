from pydantic import BaseModel,field_validator
from fastapi import Form
from typing import Optional
from datetime import datetime


class SiteCMSForm(BaseModel):
    meta_title: str
    subtitle: str
    meta_description: str
    page_content: str
    is_active: bool = True

    @classmethod
    def as_form(
        cls,
        meta_title: str = Form(...),
        subtitle: str = Form(...),
        meta_description: str = Form(...),
        page_content: str = Form(...),
        is_active: bool = Form(True),
    ):
        return cls(
            meta_title=meta_title.strip(),
            subtitle=subtitle.strip(),
            meta_description=meta_description.strip(),
            page_content=page_content,
            is_active=is_active,
        )
    

    @field_validator("meta_title", "subtitle", "meta_description", "page_content")
    @classmethod
    def required_fields(cls, v, info):
        if not v or not v.strip():
            raise ValueError(f"{info.field_name.replace('_',' ').title()} is required")
        return v
    

class SiteCMSResponse(BaseModel):
    id: int
    page_key: str

    meta_title: Optional[str]
    subtitle: Optional[str]
    meta_description: Optional[str]
    page_content: Optional[str]

    is_active: bool
    is_update: bool

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_from_attributes = True  
