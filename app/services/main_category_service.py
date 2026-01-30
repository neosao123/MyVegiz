# app/services/main_category_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.api.v1.admin.routes import main_categories
from fastapi import UploadFile
from sqlalchemy.sql import func
import uuid
import re
import cloudinary.uploader

from app.models.main_category import MainCategory
from app.schemas.main_category import MainCategoryCreate, MainCategoryUpdate
from app.core.exceptions import AppException


MAX_IMAGE_SIZE = 1 * 1024 * 1024
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]


def upload_main_category_image(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise AppException(400, "Only JPG and PNG images allowed")

    contents = file.file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise AppException(400, "Image must be less than 1MB")

    result = cloudinary.uploader.upload(
        contents,
        folder="myvegiz/main-categories",
        resource_type="image"
    )
    return result["secure_url"]


def generate_slug(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")


# ✅ CREATE
def create_main_category(
    db: Session,
    data: MainCategoryCreate,
    image: UploadFile = None
):
    slug = generate_slug(data.main_category_name)

    if db.query(MainCategory).filter(MainCategory.slug == slug).first():
        raise AppException(400, "Main category already exists")

    image_url = upload_main_category_image(image) if image else None

    category = MainCategory(
        uu_id=str(uuid.uuid4()),
        main_category_name=data.main_category_name,
        slug=slug,
        main_category_image=image_url,
        is_active=data.is_active
    )

    try:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except IntegrityError:
        db.rollback()
        raise AppException(500, "Database error")



def list_main_categories(db: Session, offset: int, limit: int):
    # -------------------------------
    # Base filters (soft delete aware)
    # -------------------------------
    base_query = db.query(MainCategory).filter(
        MainCategory.is_active == True
    ).order_by(MainCategory.created_at.desc())

    total_records = base_query.count()

    main_categories = base_query.offset(offset).limit(limit).all()

    return total_records, main_categories


# ✅ UPDATE
def update_main_category(
    db: Session,
    uu_id: str,
    data: MainCategoryUpdate,
    image: UploadFile = None
):
    category = db.query(MainCategory).filter(MainCategory.uu_id == uu_id).first()

    if not category:
        raise AppException(404, "Main category not found")

    if data.main_category_name:
        new_slug = generate_slug(data.main_category_name)
        if db.query(MainCategory).filter(
            MainCategory.slug == new_slug,
            MainCategory.uu_id != uu_id
        ).first():
            raise AppException(400, "Main category already exists")

        category.main_category_name = data.main_category_name
        category.slug = new_slug

    if data.is_active is not None:
        category.is_active = data.is_active

 # ✅ FIXED (CORRECT)
    if image and image.filename:
        print("IMAGE RECEIVED:", image.filename if image else None)
        category.main_category_image = upload_main_category_image(image)
    category.is_update = True
    category.updated_at = func.now()

    db.commit()
    db.refresh(category)
    return category
