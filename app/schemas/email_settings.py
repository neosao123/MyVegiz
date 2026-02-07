from pydantic import BaseModel, EmailStr, field_validator
from fastapi import Form
from typing import Optional
from datetime import datetime


# -------------------------
# EMAIL SETTINGS CREATE
# -------------------------
class EmailSettingCreate(BaseModel):
    protocol: str
    host: str
    port: int
    encryption: str
    username: str
    password: str
    from_name: str
    from_email: EmailStr

    # -------------------------
    # FORM SUPPORT
    # Allows multipart/form-data submission
    # -------------------------
    @classmethod
    def as_form(
        cls,
        protocol: str = Form(...),
        host: str = Form(...),
        port: int = Form(...),
        encryption: str = Form(...),
        username: str = Form(...),
        password: str = Form(...),
        from_name: str = Form(...),
        from_email: EmailStr = Form(...),
    ):
        return cls(
            protocol=protocol,
            host=host,
            port=port,
            encryption=encryption,
            username=username,
            password=password,
            from_name=from_name,
            from_email=from_email,
        )

# -------------------------
# EMAIL SETTINGS RESPONSE
# -------------------------
class EmailSettingResponse(BaseModel):
    id: int
    protocol: str
    host: str
    port: int
    encryption: str
    username: str
    password: str
    from_name: str
    from_email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True


# -------------------------
# TEST EMAIL REQUEST
# -------------------------
class TestEmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    message: str

    @classmethod
    def as_form(
        cls,
        to_email: EmailStr = Form(...),
        subject: str = Form(...),
        message: str = Form(...),
    ):
        return cls(
            to_email=to_email,
            subject=subject,
            message=message,
        )
