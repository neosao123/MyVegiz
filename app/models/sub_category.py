from sqlalchemy import Column, Integer, String, Boolean, DateTime,ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship


class SubCategory(Base):
    __tablename__ = "sub_categories"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        index=True
    )
    uu_id = Column(String(255), unique=True, index=True, nullable=False)
    sub_category_name = Column(String(255), nullable=False)
    slug = Column(String(255), index=True, nullable=False)
    sub_category_image = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)
    is_update = Column(Boolean, default=False)
    is_delete = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)


