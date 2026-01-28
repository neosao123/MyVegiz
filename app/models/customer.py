from sqlalchemy import Column, Integer, String, Boolean, DateTime,ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


# Update your Customer model
class Customer(Base):

    __tablename__ = "customers"


    id = Column(Integer, primary_key=True, index=True)
    uu_id = Column(String(255), unique=True, index=True, nullable=False)

    name = Column(String(255), nullable=False)
    email = Column(String(255),index=True, nullable=False)
    contact = Column(String(20), nullable=True)
    password = Column(String(255), nullable=False)
   
    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    is_update = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    


