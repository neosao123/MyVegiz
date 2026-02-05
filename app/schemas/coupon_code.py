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

# -------------------------
# COUPON CREATE SCHEMA
# -------------------------
class CouponCodeCreate(BaseModel):
    coupon_code: str
    coupon_type: str          # flat | percentile
    disc_value: int
    cap_limit: Optional[int] = None
    order_value: int
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
        coupon_type: str = Form(...),
        disc_value: int = Form(...),
        cap_limit: Optional[int] = Form(None),
        order_value: int = Form(...),
        termscondition: Optional[str] = Form(None),
        coupon_description: Optional[str] = Form(None),
        use_limit: int = Form(...),
        expiry_date: datetime = Form(...),
        is_active: bool = Form(True),
    ):
        return cls(
            coupon_code=coupon_code.strip(),
            coupon_type=coupon_type,
            disc_value=disc_value,
            cap_limit=cap_limit,
            order_value=order_value,
            termscondition=termscondition,
            coupon_description=coupon_description,
            use_limit=use_limit,
            expiry_date=expiry_date,
            is_active=is_active
        )

    # ---------- REQUIRED FIELD CHECK ----------
    @field_validator("coupon_code", "coupon_type","disc_value","order_value","use_limit", "expiry_date", mode="before")
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
    
    # ---------- COUPON TYPE ----------
    @field_validator("coupon_type")
    @classmethod
    def validate_coupon_type(cls, v):
        if v not in ["flat", "percentile"]:
            raise ValueError("Coupon type must be flat or percentile")
        return v


    # ---------- ORDER VALUE ----------
    @field_validator("order_value")
    @classmethod
    def validate_order_value(cls, v):
        if v <= 0:
            raise ValueError("Order value must be greater than zero")
        return v


    # ---------- DISCOUNT VALUE ----------
    @field_validator("disc_value")
    @classmethod
    def validate_disc_value(cls, v, info):
        coupon_type = info.data.get("coupon_type")

        if v <= 0:
            raise ValueError("Discount value must be greater than zero")

        if coupon_type == "percentile" and v > 100:
            raise ValueError("Percentile must be between 1 and 100")

        return v

    # ---------- CAP LIMIT ----------
    @field_validator("cap_limit")
    @classmethod
    def validate_cap_limit(cls, cap_limit, info):
        coupon_type = info.data.get("coupon_type")

        if coupon_type == "percentile" and cap_limit is None:
            raise ValueError("Cap limit is required for percentile coupon")

        if coupon_type == "flat" and cap_limit is not None:
            raise ValueError("Cap limit not allowed for flat coupon")

        return cap_limit


    # ---------- USE LIMIT ----------
    @field_validator("use_limit")
    @classmethod
    def validate_use_limit(cls, v):
        if v < 0:
            raise ValueError("Use limit must be greater than or equal to zero")
        return v

   
    
    # ---------- EXPIRY DATE ----------
    @field_validator("expiry_date")
    @classmethod
    def validate_expiry_date(cls, v: datetime):
        if v.date() < datetime.today().date():
            raise ValueError("Expiry date must be today or a future date")
        return v

    


# -------------------------
# COUPON RESPONSE SCHEMA
# -------------------------
class CouponCodeResponse(BaseModel):
    id: int
    uu_id: str
    coupon_code: str

    coupon_type: Optional[str] = None
    disc_value: Optional[int] = None
    cap_limit: Optional[int] = None
    order_value: Optional[int] = None

    termscondition: Optional[str]
    coupon_description: Optional[str]
    use_limit: int
    expiry_date: datetime
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True

 
# -------------------------
# COUPON UPDATE SCHEMA
# -------------------------
class CouponCodeUpdate(BaseModel):
    coupon_code: Optional[str] = None
    coupon_type: Optional[str] = None        # flat | percentile
    disc_value: Optional[int] = None
    cap_limit: Optional[int] = None
    order_value: Optional[int] = None
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
        coupon_type: Optional[str] = Form(None),
        disc_value: Optional[int] = Form(None),
        cap_limit: Optional[int] = Form(None),
        order_value: Optional[int] = Form(None),
        termscondition: Optional[str] = Form(None),
        coupon_description: Optional[str] = Form(None),
        use_limit: Optional[int] = Form(None),
        expiry_date: Optional[datetime] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            coupon_code=coupon_code.strip() if coupon_code else None,
            coupon_type=coupon_type,
            disc_value=disc_value,
            cap_limit=cap_limit,
            order_value=order_value,
            termscondition=termscondition.strip() if termscondition else None,
            coupon_description=coupon_description.strip() if coupon_description else None,
            use_limit=use_limit,
            expiry_date=expiry_date,
            is_active=is_active,
        )

    # ---------- VALIDATIONS ----------

    @field_validator("coupon_code")
    @classmethod
    def validate_coupon_code(cls, v):
        if v and len(v) < 3:
            raise ValueError("Coupon code must be at least 3 characters")
        return v

    @field_validator("coupon_type")
    @classmethod
    def validate_coupon_type(cls, v):
        if v and v not in ["flat", "percentile"]:
            raise ValueError("Coupon type must be flat or percentile")
        return v

    @field_validator("disc_value")
    @classmethod
    def validate_disc_value(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Discount value must be greater than zero")
        return v

    @field_validator("use_limit")
    @classmethod
    def validate_use_limit(cls, v):
        if v is not None and v < 0:
            raise ValueError("Use limit must be greater than or equal to zero")
        return v

    @field_validator("order_value")
    @classmethod
    def validate_order_value(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Order value must be greater than zero")
        return v

    @field_validator("expiry_date")
    @classmethod
    def validate_expiry_date(cls, v):
        if v and v.date() < datetime.today().date():
            raise ValueError("Expiry date must be today or future")
        return v

    # ---------- BUSINESS RULE (CORE) ----------
    @field_validator("cap_limit")
    @classmethod
    def validate_discount_logic(cls, cap_limit, info):
        data = info.data
        coupon_type = data.get("coupon_type")
        disc_value = data.get("disc_value")

        if coupon_type == "percentile":
            if disc_value is not None and disc_value > 100:
                raise ValueError("Percentile must be between 1 and 100")
            if cap_limit is None:
                raise ValueError("Cap limit is required for percentile coupon")

        if coupon_type == "flat" and cap_limit is not None:
            raise ValueError("Cap limit not allowed for flat coupon")

        return cap_limit
