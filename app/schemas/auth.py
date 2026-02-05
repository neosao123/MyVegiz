from pydantic import BaseModel, EmailStr, field_validator
import re

# -------------------------
# LOGIN REQUEST SCHEMA
# -------------------------
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

# -------------------------
# USER DATA RETURNED ON LOGIN
# -------------------------
class UserLoginData(BaseModel):
    id: int
    email: EmailStr
    name: str
    contact:str
    profile_image:str
    is_admin:bool
    uu_id:str
    is_active:bool

# -------------------------
# LOGIN RESPONSE SCHEMA
# -------------------------
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserLoginData   #  login details

# -------------------------
# REFRESH TOKEN REQUEST
# -------------------------
class RefreshTokenRequest(BaseModel):
    refresh_token: str