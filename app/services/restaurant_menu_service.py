from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import uuid

from app.models.menu import Menu
from app.schemas.restaurant_menu import MenuCreate, MenuUpdate
from app.core.exceptions import AppException


# -------------------------
# CODE GENERATOR
# -------------------------
def generate_menu_code(db: Session) -> str:
    last = db.query(Menu).order_by(Menu.id.desc()).first()
    next_id = last.id + 1 if last else 1
    return f"MENU_{next_id}"


# -------------------------
# CREATE
# -------------------------
def create_menu(db: Session, data: MenuCreate):
    exists = db.query(Menu).filter(
        Menu.menu == data.menu,
        Menu.is_delete == False
    ).first()

    if exists:
        raise AppException(400, "Menu already exists")

    menu = Menu(
        uu_id=str(uuid.uuid4()),
        code=generate_menu_code(db),
        menu=data.menu,
        priority=data.priority or 0,
        is_active=data.is_active
    )

    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


# -------------------------
# LIST
# -------------------------
def list_menus(db: Session, offset: int, limit: int):
    base_query = db.query(Menu).filter(
        Menu.is_delete == False
    ).order_by(Menu.priority.asc(), Menu.created_at.desc())

    total_records = base_query.count()
    data = base_query.offset(offset).limit(limit).all()

    return total_records, data


# -------------------------
# UPDATE
# -------------------------
def update_menu(db: Session, uu_id: str, data: MenuUpdate):
    menu = db.query(Menu).filter(
        Menu.uu_id == uu_id,
        Menu.is_delete == False
    ).first()

    if not menu:
        raise AppException(404, "Menu not found")

    if data.menu:
        exists = db.query(Menu).filter(
            Menu.menu == data.menu,
            Menu.uu_id != uu_id,
            Menu.is_delete == False
        ).first()
        if exists:
            raise AppException(400, "Menu already exists")

        menu.menu = data.menu

    if data.priority is not None:
        menu.priority = data.priority

    if data.is_active is not None:
        menu.is_active = data.is_active

    menu.is_update = True
    menu.updated_at = func.now()

    db.commit()
    db.refresh(menu)
    return menu


# -------------------------
# DELETE (SOFT)
# -------------------------
def delete_menu(db: Session, uu_id: str):
    menu = db.query(Menu).filter(
        Menu.uu_id == uu_id,
        Menu.is_delete == False
    ).first()

    if not menu:
        raise AppException(404, "Menu not found")

    menu.is_delete = True
    menu.is_active = False
    menu.deleted_at = func.now()
    menu.updated_at = func.now()

    db.commit()
    db.refresh(menu)
    return menu
