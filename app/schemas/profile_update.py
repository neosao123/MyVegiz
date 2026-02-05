from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional


# =========================================================
# USER UPDATE SCHEMA
# Used to update user profile information
# All fields are optional
# =========================================================
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    contact: Optional[str] = None
    password: Optional[str] = None

  # -----------------------------------------------------
    # FORM SUPPORT
    # Enables multipart/form-data submission
    # -----------------------------------------------------
    @classmethod
    def as_form(
        cls,
        name: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        contact: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
    ):
        return cls(
            name=name.strip() if name else None,
            email=email.strip().lower() if email else None,
            contact=contact.strip() if contact else None,
            password=password,
        )

    # ---------- VALIDATIONS ----------
    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if v is not None and len(v) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v is not None and "@" not in v:
            raise ValueError("Invalid email address")
        return v

    @field_validator("contact")
    @classmethod
    def validate_contact(cls, v):
        if v is not None and len(v) < 10:
            raise ValueError("Contact number must be at least 10 digits")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if v is not None and len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v
