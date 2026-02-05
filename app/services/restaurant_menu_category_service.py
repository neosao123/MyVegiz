from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import uuid

from app.models.menu_category import MenuCategory
from app.models.menu import Menu

from app.schemas.restaurant_menu_category import (
    MenuCategoryCreate,
    MenuCategoryUpdate
)
from app.core.exceptions import AppException


# =====================================================
# MENU CATEGORY CODE GENERATOR
# Generates sequential codes like MCAT_1, MCAT_2
# =====================================================
def generate_menu_category_code(db: Session) -> str:
    last = db.query(MenuCategory).order_by(MenuCategory.id.desc()).first()
    next_id = last.id + 1 if last else 1
    return f"MCAT_{next_id}"


# =====================================================
# CREATE MENU CATEGORY
# =====================================================
def create_menu_category(db: Session, data: MenuCategoryCreate):
    exists = db.query(MenuCategory).filter(
        MenuCategory.menu_category == data.menu_category,
        MenuCategory.menu_id == data.menu_id,
        MenuCategory.is_delete == False
    ).first()

    if exists:
        raise AppException(400, "Menu category already exists")

    entity = MenuCategory(
        uu_id=str(uuid.uuid4()),
        code=generate_menu_category_code(db),
        menu_id=data.menu_id,
        menu_category=data.menu_category,
        is_active=data.is_active
    )

    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


# =====================================================
# LIST MENU CATEGORIES (PAGINATED)
# Optional filter by menu_id
# =====================================================
def list_menu_categories(db: Session, offset: int, limit: int, menu_id: int | None = None):
    base_query = db.query(MenuCategory).filter(
        MenuCategory.is_delete == False
    ).order_by(MenuCategory.created_at.desc())

    if menu_id:
        base_query = base_query.filter(MenuCategory.menu_id == menu_id)

    total = base_query.count()
    data = base_query.offset(offset).limit(limit).all()
    return total, data


# =====================================================
# UPDATE MENU CATEGORY
# =====================================================
def update_menu_category(db: Session, uu_id: str, data: MenuCategoryUpdate):
    entity = db.query(MenuCategory).filter(
        MenuCategory.uu_id == uu_id,
        MenuCategory.is_delete == False
    ).first()

    if not entity:
        raise AppException(404, "Menu category not found")

    if data.menu_category:
        exists = db.query(MenuCategory).filter(
            MenuCategory.menu_category == data.menu_category,
            MenuCategory.menu_id == entity.menu_id,
            MenuCategory.uu_id != uu_id,
            MenuCategory.is_delete == False
        ).first()

        if exists:
            raise AppException(400, "Menu category already exists")

        entity.menu_category = data.menu_category

    if data.is_active is not None:
        entity.is_active = data.is_active

    entity.is_update = True
    entity.updated_at = func.now()

    db.commit()
    db.refresh(entity)
    return entity


# =====================================================
# DELETE MENU CATEGORY (SOFT DELETE)
# =====================================================
def delete_menu_category(db: Session, uu_id: str):
    entity = db.query(MenuCategory).filter(
        MenuCategory.uu_id == uu_id,
        MenuCategory.is_delete == False
    ).first()

    if not entity:
        raise AppException(404, "Menu category not found")

    entity.is_delete = True
    entity.is_active = False
    entity.deleted_at = func.now()
    entity.updated_at = func.now()

    db.commit()
    db.refresh(entity)
    return entity

# =====================================================
# MENU DROPDOWN LIST
# Returns only active & non-deleted menus
# Used for dropdown selections
# =====================================================
def list_menu_dropdown(db: Session):
    menus = db.query(Menu).filter(
        Menu.is_delete == False,
        Menu.is_active == True
    ).order_by(Menu.menu.asc()).all()

    return menus