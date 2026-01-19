from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class UOM(Base):
    __tablename__ = "uoms"

    id = Column(Integer, primary_key=True, index=True)
    uom_code = Column(String(255),unique=True, index=True, nullable=False)

    uom_name = Column(String(255), nullable=False)
    uom_short_name = Column(String(255), index=True, nullable=False)
    description = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    is_update = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
