from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class MobileOTP(Base):
    __tablename__ = "mobile_otp"


    id = Column(Integer, primary_key=True, index=True)
    mobile = Column(String(20), index=True, nullable=False)  
    otp = Column(String(6), nullable=False)

    is_verified = Column(Boolean, default=False)

    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    