from sqlalchemy import Column, Integer, String, Boolean, DateTime,ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship


class EntityCategory(Base):
    __tablename__ = "entity_categories"

    id = Column(Integer, primary_key=True, index=True)
    uu_id = Column(String(255), unique=True, index=True, nullable=False)
    code = Column(String(100), unique=True, index=True, nullable=False)

    main_category_id = Column(
        Integer,
        ForeignKey("main_categories.id"),
        index=True
    )
    entity_category = Column(String(255), nullable=False)


    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    is_update = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

