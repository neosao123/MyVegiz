from sqlalchemy import Column, Integer, String, Boolean, DateTime,ForeignKey,Text
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        index=True
    )
    sub_category_id = Column(
        Integer,
        ForeignKey("sub_categories.id"),
        nullable=True, 
        index=True
    )
    product_name = Column(String(255), nullable=False)
    product_short_name = Column(String(255), index=True, nullable=False)
    
    uu_id = Column(String(255), unique=True, index=True, nullable=False)
    slug = Column(String(255), index=True, nullable=False)

    short_description = Column(String(255), nullable=True)
    long_description = Column(Text, nullable=True)
    hsn_code = Column(String(255), nullable=True)
    sku_code = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    is_update = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    

    # ✅ ADD THIS
    images = relationship(
        "ProductImage",
        backref="product",
        cascade="all, delete-orphan"
    )

    # 🔗 RELATIONSHIPS
    category = relationship("Category")
    sub_category = relationship("SubCategory")