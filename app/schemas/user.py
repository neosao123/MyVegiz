from pydantic import BaseModel, EmailStr,field_validator, Field, validator
from fastapi import Form
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
    is_admin: bool = False


    # 
    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        email: str = Form(...),
        contact: str = Form(...),
        password: str = Form(...),
        is_admin: bool = Form(False),
    ):
        return cls(
            name=name,
            email=email,
            contact=contact,
            password=password,
            is_admin=is_admin,
        )


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
        orm_from_attributes = True




class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    contact: Optional[str] = None
    password: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        name: Optional[str] = Form(None),
        email: Optional[EmailStr] = Form(None),
        contact: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
    ):
        return cls(
            name=name.strip() if name and name.strip() else None,          
            email=email.strip() if email and email.strip() else None,  # ✅
            contact=contact.strip() if contact and contact.strip() else None,  # ✅
            password=password.strip() if password and password.strip() else None,  # ✅
        )

    # ---------- VALIDATIONS ----------
    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if v is not None:
            v = v.strip()  # ✅ Strip it first
            if not v:
                raise ValueError("Name is required")
            if len(v) < 3:
                raise ValueError("Name must be at least 3 characters long")
        return v  # ✅ Return the stripped value



    @field_validator("contact")
    @classmethod
    def validate_contact(cls, v):
        if v is not None:
            v = v.strip()  # ✅ Add this
            if not v.isdigit():
                raise ValueError("Contact must contain only digits")
            if len(v) != 10:
                raise ValueError("Contact number must be exactly 10 digits")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if v is not None:
            v = v.strip()  # ✅ Add this
            if len(v) < 8:
                raise ValueError("Password must be at least 8 characters long")
        return v