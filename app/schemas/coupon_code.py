from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional
from datetime import datetime
from typing import Optional


from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional
from datetime import datetime
import re


class CouponCodeCreate(BaseModel):
    coupon_code: str
    flat: Optional[int] = None
    percentile: Optional[int] = None
    cap_limit: Optional[int] = None
    termscondition: Optional[str] = None
    coupon_description: Optional[str] = None
    use_limit: int
    expiry_date: datetime
    is_active: bool = True

    # ---------------- FORM ----------------
    @classmethod
    def as_form(
        cls,
        coupon_code: str = Form(...),
        flat: Optional[int] = Form(None),
        percentile: Optional[int] = Form(None),
        cap_limit: Optional[int] = Form(None),
        termscondition: Optional[str] = Form(None),
        coupon_description: Optional[str] = Form(None),
        use_limit: int = Form(...),
        expiry_date: datetime = Form(...),
        is_active: bool = Form(True),
    ):
        return cls(
            coupon_code=coupon_code.strip(),
            flat=flat,
            percentile=percentile,
            cap_limit=cap_limit,
            termscondition=termscondition.strip() if termscondition else None,
            coupon_description=coupon_description.strip() if coupon_description else None,
            use_limit=use_limit,
            expiry_date=expiry_date,
            is_active=is_active,
        )

    # ---------- REQUIRED FIELD CHECK ----------
    @field_validator("coupon_code", "use_limit", "expiry_date", mode="before")
    @classmethod
    def required_fields(cls, value, info):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError(f"{info.field_name.replace('_', ' ').title()} is required")
        return value

    # ---------- COUPON CODE ----------
    @field_validator("coupon_code")
    @classmethod
    def validate_coupon_code(cls, v):
        if len(v) < 3:
            raise ValueError("Coupon code must be at least 3 characters")
        return v

    # ---------- USE LIMIT ----------
    @field_validator("use_limit")
    @classmethod
    def validate_use_limit(cls, v):
        if v < 0:
            raise ValueError("Use limit must be greater than or equal to zero")
        return v

    # ---------- PERCENTILE ----------
    @field_validator("percentile")
    @classmethod
    def validate_percentile(cls, v):
        if v is not None and (v <= 0 or v > 100):
            raise ValueError("Percentile must be between 1 and 100")
        return v
    

    @field_validator("expiry_date")
    @classmethod
    def validate_expiry_date(cls, v: datetime):
        if v.date() < datetime.today().date():
            raise ValueError("Expiry date must be today or a future date")
        return v



    # ---------- BUSINESS RULES ----------
    @field_validator("cap_limit")
    @classmethod
    def validate_discount_logic(cls, cap_limit, info):
        values = info.data
        flat = values.get("flat")
        percentile = values.get("percentile")

        if flat and percentile:
            raise ValueError("Only one of flat or percentile is allowed")

        if not flat and not percentile:
            raise ValueError("Either flat or percentile is required")

        if percentile and cap_limit is None:
            raise ValueError("Cap limit is required when using percentile")

        if flat and cap_limit is not None:
            raise ValueError("Cap limit is not allowed when using flat discount")

        return cap_limit
    


class CouponCodeResponse(BaseModel):
    id: int
    uu_id: str
    coupon_code: str
    flat: Optional[int]
    percentile: Optional[int]
    cap_limit: Optional[int]
    termscondition: Optional[str]
    coupon_description: Optional[str]
    use_limit: int
    expiry_date: datetime
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True   



class CouponCodeUpdate(BaseModel):
    coupon_code: Optional[str] = None
    flat: Optional[int] = None
    percentile: Optional[int] = None
    cap_limit: Optional[int] = None
    termscondition: Optional[str] = None
    coupon_description: Optional[str] = None
    use_limit: Optional[int] = None
    expiry_date: Optional[datetime] = None
    is_active: Optional[bool] = None

    # ---------------- FORM ----------------
    @classmethod
    def as_form(
        cls,
        coupon_code: Optional[str] = Form(None),
        flat: Optional[int] = Form(None),
        percentile: Optional[int] = Form(None),
        cap_limit: Optional[int] = Form(None),
        termscondition: Optional[str] = Form(None),
        coupon_description: Optional[str] = Form(None),
        use_limit: Optional[int] = Form(None),
        expiry_date: Optional[datetime] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            coupon_code=coupon_code.strip() if coupon_code else None,
            flat=flat,
            percentile=percentile,
            cap_limit=cap_limit,
            termscondition=termscondition.strip() if termscondition else None,
            coupon_description=coupon_description.strip() if coupon_description else None,
            use_limit=use_limit,
            expiry_date=expiry_date,
            is_active=is_active,
        )
    

    @field_validator("coupon_code")
    @classmethod
    def validate_coupon_code(cls, v):
        if v and len(v) < 3:
            raise ValueError("Coupon code must be at least 3 characters")
        return v

    @field_validator("use_limit")
    @classmethod
    def validate_use_limit(cls, v):
        if v is not None and v < 0:
            raise ValueError("Use limit must be greater than or equal to zero")
        return v

    @field_validator("percentile")
    @classmethod
    def validate_percentile(cls, v):
        if v is not None and (v <= 0 or v > 100):
            raise ValueError("Percentile must be between 1 and 100")
        return v

    @field_validator("expiry_date")
    @classmethod
    def validate_expiry_date(cls, v):
        if v and v.date() < datetime.today().date():
            raise ValueError("Expiry date must be today or a future date")
        return v

    # ---------- BUSINESS RULES ----------
    @field_validator("cap_limit")
    @classmethod
    def validate_discount_logic(cls, cap_limit, info):
        values = info.data
        flat = values.get("flat")
        percentile = values.get("percentile")

        if flat and percentile:
            raise ValueError("Only one of flat or percentile is allowed")
        
        if not flat and not percentile:
            raise ValueError("Either flat or percentile is required")

        if percentile and cap_limit is None:
            raise ValueError("Cap limit is required when using percentile")

        if flat and cap_limit is not None:
            raise ValueError("Cap limit is not allowed for flat discount")

        return cap_limit

