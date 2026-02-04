from sqlalchemy import Column, Integer, String, Boolean, DateTime,ForeignKey,Float,Text
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship

from app.models.menu import Menu
from app.models.menu_category import MenuCategory

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    uu_id = Column(String(255), unique=True, index=True, nullable=False)

    code = Column(String(100), unique=True, index=True, nullable=False)

    menu_id = Column(
        Integer,
        ForeignKey("menus.id"),
        index=True
    )

    menu_category_id = Column(
        Integer,
        ForeignKey("menu_categories.id"),
        index=True
    )


    item = Column(String(255), nullable=False)

    sale_price = Column(Float, nullable=False)
    packing_charges = Column(Float, default=0.0)

    max_order_quantity = Column(Integer, default=1)

    cuisine_type = Column(String(100), nullable=True)

    item_image = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    item_status = Column(
        String(50),
        default="available"  # available / unavailable / out_of_stock
    )

    is_approved = Column(Boolean, default=False)
    
    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    is_update = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    menu = relationship("Menu")
    menu_category = relationship("MenuCategory")