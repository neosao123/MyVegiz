from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import uuid

from app.models.menu_item import MenuItem
from app.schemas.restaurant_menu_item import (
    MenuItemCreate,
    MenuItemUpdate
)
from app.core.exceptions import AppException
from fastapi import UploadFile
import cloudinary.uploader

from app.models.menu import Menu
from app.models.menu_category import MenuCategory



MAX_IMAGE_SIZE = 1 * 1024 * 1024
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]

def upload_menu_item_image(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise AppException(400, "Only JPG and PNG images allowed")

    contents = file.file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise AppException(400, "Image must be less than 1MB")

    result = cloudinary.uploader.upload(
        contents,
        folder="myvegiz/menu_items",
        resource_type="image"
    )
    return result["secure_url"]


# -------------------------
# CODE GENERATOR
# -------------------------
def generate_menu_item_code(db: Session) -> str:
    last = db.query(MenuItem).order_by(MenuItem.id.desc()).first()
    next_id = last.id + 1 if last else 1
    return f"ITEM_{next_id}"


# -------------------------
# CREATE
# -------------------------
def create_menu_item(
    db: Session,
    data: MenuItemCreate,
    item_image: UploadFile = None
):
    # -------------------------
    # MENU VALIDATION
    # -------------------------
    menu = db.query(Menu).filter(
        Menu.id == data.menu_id,
        Menu.is_delete == False,
        Menu.is_active == True
    ).first()

    if not menu:
        raise AppException(400, "Menu not found")

    # -------------------------
    # MENU CATEGORY VALIDATION (OPTIONAL)
    # -------------------------
    if data.menu_category_id is not None:
        category = db.query(MenuCategory).filter(
            MenuCategory.id == data.menu_category_id,
            MenuCategory.is_delete == False,
            MenuCategory.is_active == True
        ).first()

        if not category:
            raise AppException(400, "Menu category not found")

    # -------------------------
    # DUPLICATE CHECK
    # -------------------------
    exists = db.query(MenuItem).filter(
        MenuItem.item == data.item,
        MenuItem.menu_id == data.menu_id,
        MenuItem.is_delete == False
    ).first()

    if exists:
        raise AppException(400, "Menu item already exists")

    # -------------------------
    # IMAGE UPLOAD
    # -------------------------
    image_url = upload_menu_item_image(item_image) if item_image else None

    # -------------------------
    # CREATE ITEM
    # -------------------------
    item = MenuItem(
        uu_id=str(uuid.uuid4()),
        code=generate_menu_item_code(db),
        item=data.item,
        sale_price=data.sale_price,
        packing_charges=data.packing_charges,
        max_order_quantity=data.max_order_quantity,
        cuisine_type=data.cuisine_type,
        menu_id=data.menu_id,
        menu_category_id=data.menu_category_id,
        description=data.description,
        item_image=image_url,
        item_status=data.item_status or "available",
        is_approved=data.is_approved if data.is_approved is not None else False,
        is_active=data.is_active
    )

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# -------------------------
# LIST
# -------------------------
def list_menu_items(
    db: Session,
    offset: int,
    limit: int,
    menu_id: int | None = None
):
    base_query = db.query(MenuItem).filter(
        MenuItem.is_delete == False
    ).order_by(MenuItem.created_at.desc())

    if menu_id:
        base_query = base_query.filter(MenuItem.menu_id == menu_id)

    total_records = base_query.count()
    data = base_query.offset(offset).limit(limit).all()

    return total_records, data


# -------------------------
# UPDATE
# -------------------------
def update_menu_item(
    db: Session,
    uu_id: str,
    data: MenuItemUpdate,
    item_image: UploadFile = None
):
    item = db.query(MenuItem).filter(
        MenuItem.uu_id == uu_id,
        MenuItem.is_delete == False
    ).first()

    if not item:
        raise AppException(404, "Menu item not found")
    
    # MENU VALIDATION
    if data.menu_id is not None:
        menu = db.query(Menu).filter(
            Menu.id == data.menu_id,
            Menu.is_delete == False,
            Menu.is_active == True
        ).first()

        if not menu:
            raise AppException(400, "Menu not found")

        item.menu_id = data.menu_id


    # MENU CATEGORY VALIDATION
    if data.menu_category_id is not None:
        category = db.query(MenuCategory).filter(
            MenuCategory.id == data.menu_category_id,
            MenuCategory.is_delete == False,
            MenuCategory.is_active == True
        ).first()

        if not category:
            raise AppException(400, "Menu category not found")

        item.menu_category_id = data.menu_category_id

    # Update remaining fields
    for field, value in data.dict(
        exclude_unset=True,
        exclude={"menu_id", "menu_category_id"}
    ).items():
        setattr(item, field, value)


    if item_image:
        item.item_image = upload_menu_item_image(item_image)

    item.is_update = True
    item.updated_at = func.now()

    db.commit()
    db.refresh(item)
    return item



# -------------------------
# DELETE (SOFT)
# -------------------------
def delete_menu_item(db: Session, uu_id: str):
    item = db.query(MenuItem).filter(
        MenuItem.uu_id == uu_id,
        MenuItem.is_delete == False
    ).first()

    if not item:
        raise AppException(404, "Menu item not found")

    item.is_delete = True
    item.is_active = False
    item.deleted_at = func.now()
    item.updated_at = func.now()

    db.commit()
    db.refresh(item)
    return item



# -------------------------
# MENU DROPDOWN
# -------------------------
def get_menu_dropdown(db: Session):
    return db.query(Menu).filter(
        Menu.is_delete == False,
        Menu.is_active == True
    ).order_by(Menu.priority.asc(), Menu.menu.asc()).all()


# -------------------------
# MENU CATEGORY DROPDOWN
# -------------------------
def get_menu_category_dropdown(db: Session, menu_id: int):
    return db.query(MenuCategory).filter(
        MenuCategory.menu_id == menu_id,
        MenuCategory.is_delete == False,
        MenuCategory.is_active == True
    ).order_by(MenuCategory.menu_category.asc()).all()
