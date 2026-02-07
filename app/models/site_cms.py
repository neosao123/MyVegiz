from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base


class SiteCMS(Base):
    __tablename__ = "site_cms"

    id = Column(Integer, primary_key=True, index=True)

    # Identify CMS page (terms,privacypolicy,refund)
    page_key = Column(String(50), nullable=False, index=True)

    meta_title = Column(String(255), nullable=True)
    subtitle = Column(String(255), nullable=True)

    meta_description = Column(Text, nullable=True)
    page_content = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    is_update = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<SiteCMS id={self.id} page_key={self.page_key}>"
