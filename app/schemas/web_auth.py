from pydantic import BaseModel, EmailStr, field_validator

# ============================================================
# WEB REGISTER REQUEST SCHEMA
# ============================================================
class WebRegisterRequest(BaseModel):
    name: str
    # email: EmailStr
    contact: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return v.strip()

    @field_validator("contact")
    @classmethod
    def validate_contact(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError("Invalid contact number")
        return v


from pydantic import BaseModel
from typing import Optional

# ============================================================
# MOBILE SIGN-IN REQUEST SCHEMA
# ============================================================
class MobileSignInRequest(BaseModel):
    mobile: str


# ============================================================
# MOBILE OTP VERIFY REQUEST SCHEMA
# ============================================================
class MobileOTPVerifyRequest(BaseModel):
    mobile: str
    otp: str



# ============================================================
# CUSTOMER RESPONSE SCHEMA
# ============================================================
class CustomerResponse(BaseModel):
    id: int
    uu_id: str
    name: str
    # email: Optional[str] = None
    contact: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True



# ============================================================
# OTP LOGIN RESPONSE SCHEMA
# ============================================================
class OTPResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    customer: CustomerResponse
