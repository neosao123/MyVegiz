from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class CouponCode(Base):
    __tablename__ = "coupon_codes"

    id = Column(Integer, primary_key=True, index=True)
    uu_id = Column(String(255), unique=True, index=True, nullable=False)

    coupon_code = Column(String(100), unique=True, nullable=False)

    flat = Column(Integer, nullable=True)          # Flat discount amount
    percentile = Column(Integer, nullable=True)    # Percentage discount
    cap_limit = Column(Integer, nullable=True)     # Max discount limit

    termscondition = Column(String(1000), nullable=True)     # textarea
    coupon_description = Column(String(1000), nullable=True) # textarea

    use_limit = Column(Integer, nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=False)

    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    is_update = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
