from sqlalchemy import Column, Integer, String, Boolean, DateTime,ForeignKey,Float
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship


class ProductVariants(Base):
    __tablename__ = "product_variants"

    id = Column(Integer, primary_key=True, index=True)
    uu_id = Column(String(255), unique=True, index=True, nullable=False)

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        index=True
    )

    uom_id = Column(
        Integer,
        ForeignKey("uoms.id"),
        index=True
    )

    zone_id = Column(
        Integer,
        ForeignKey("zones.id"),
        index=True
    )

    actual_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False, index=True)

    is_deliverable=Column(Boolean, default=True)

    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    is_update = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    product = relationship("Product")
    uom = relationship("UOM")
