from pydantic import BaseModel, EmailStr, field_validator
import re

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

     # ---------- REQUIRED FIELD CHECKS (RUN FIRST) ----------
    @field_validator("email", "password", mode="before")
    @classmethod
    def required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError(f"{info.field_name.capitalize()} is required")
        return value

    # ---------- PASSWORD ----------
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str