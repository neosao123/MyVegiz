from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Control what comes in and what goes out
# Controls response format
# Hides sensitive data

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    contact: Optional[str] = None
    password: str
    profile_image: Optional[str] = None
    is_admin: bool = False


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    contact: Optional[str]
    profile_image: Optional[str]
    is_admin: bool
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
