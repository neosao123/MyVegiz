from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional
from datetime import datetime
import re


# =========================================================
# UOM CREATE SCHEMA
# Used to create a new Unit of Measurement
# =========================================================
class UOMCreate(BaseModel):
    uom_name: str
    uom_short_name: str
    description: Optional[str] = None
    is_active: bool = True

    # -----------------------------------------------------
    # FORM SUPPORT
    # Enables multipart/form-data submission
    # -----------------------------------------------------
    @classmethod
    def as_form(
        cls,
        uom_name: str = Form(...),
        uom_short_name: str = Form(...),
        description: Optional[str] = Form(None),
        is_active: bool = Form(True),
    ):
        return cls(
            uom_name=uom_name,
            uom_short_name=uom_short_name,
            description=description,
            is_active=is_active,
        )

    # ---------- REQUIRED ----------
    @field_validator("uom_name", "uom_short_name", mode="before")
    @classmethod
    def required_fields(cls, v):
        if v is None or not v.strip():
            raise ValueError("This field is required")
        return v.strip()

    # ---------- FORMAT ----------
    @field_validator("uom_name")
    @classmethod
    def validate_uom_name(cls, v):
        if len(v) < 3:
            raise ValueError("UOM name must be at least 2 characters")
        return v

    @field_validator("uom_short_name")
    @classmethod
    def validate_short_name(cls, v):
        if not re.match(r"^[A-Za-z0-9]+$", v):
            raise ValueError("UOM short name must be alphanumeric")
        return v.upper()


# =========================================================
# UOM UPDATE SCHEMA
# Used to update existing UOM data
# All fields are optional
# =========================================================
class UOMUpdate(BaseModel):
    uom_name: Optional[str] = None
    uom_short_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        uom_name: Optional[str] = Form(None),
        uom_short_name: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            uom_name=uom_name.strip() if uom_name else None,
            uom_short_name=uom_short_name.strip() if uom_short_name else None,
            description=description,
            is_active=is_active,
        )

    @field_validator("uom_name", "uom_short_name")
    @classmethod
    def validate_optional(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Field cannot be empty")
        return v
    

    # ---------- FORMAT VALIDATION ----------
    @field_validator("uom_name")
    @classmethod
    def validate_uom_name(cls, v):
        if v is not None and len(v) < 2:
            raise ValueError("UOM name must be at least 2 characters")
        return v

    @field_validator("uom_short_name")
    @classmethod
    def validate_short_name(cls, v):
        if v is not None:
            if not re.match(r"^[A-Za-z0-9]+$", v):
                raise ValueError("UOM short name must be alphanumeric")
            return v.upper()
        return v

# =========================================================
# UOM RESPONSE SCHEMA
# Used for API responses
# =========================================================
class UOMResponse(BaseModel):
    id: int
    uu_id: str
    uom_code: str
    uom_name: str
    uom_short_name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True
