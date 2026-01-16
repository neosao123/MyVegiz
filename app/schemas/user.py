from pydantic import BaseModel, EmailStr,field_validator, Field, validator
from typing import Optional
from datetime import datetime
import re

# Control what comes in and what goes out
# Controls response format
# Hides sensitive data

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    contact: str
    password: str
    profile_image: Optional[str] = None
    is_admin: bool = False


    # ---------- REQUIRED FIELD CHECKS (RUN FIRST) ----------
    @field_validator("name", "email", "contact", "password", mode="before")
    @classmethod
    def required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError(f"{info.field_name.capitalize()} is required")
        return value


    # ---------- NAME ----------
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long")

        if re.search(r"\d", value):
            raise ValueError("Name must not contain numbers")

        return value

    

    # ---------- CONTACT ----------
    @field_validator("contact")
    @classmethod
    def validate_contact(cls, value: str):
        if not value.isdigit():
            raise ValueError("Contact must contain only digits")

        if len(value) != 10:
            raise ValueError("Contact number must be exactly 10 digits")

        return value
    

    # ---------- PASSWORD ----------
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value
    

    # ---------------- PROFILE IMAGE ----------------
    @validator("profile_image")
    def validate_profile_image(cls, value: Optional[str]):
        if value is None:
            return value

        # Example: value = "image.jpg|512000"
        # You must send size from frontend or calculate after upload
        # Here we assume "filename|size_in_bytes"

        try:
            filename, size = value.split("|")
            size = int(size)
        except ValueError:
            raise ValueError("Invalid profile image format")

        max_size = 1 * 1024 * 1024  # 1 MB

        if size > max_size:
            raise ValueError("Profile image size must be less than 1 MB")

        return value


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
