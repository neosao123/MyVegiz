from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.api.v1.admin.routes import sub_categories
from fastapi import UploadFile
from sqlalchemy.sql import func
import uuid
import re
import cloudinary.uploader

from app.models.sub_category import SubCategory
from app.models.category import Category
from app.schemas.sub_category import SubCategoryCreate, SubCategoryUpdate
from app.core.exceptions import AppException


MAX_IMAGE_SIZE = 1 * 1024 * 1024
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]

def category_with_name_query(db):
    return (
        db.query(
            SubCategory.id,
            SubCategory.category_id,
            Category.category_name.label("category_name"),
            SubCategory.uu_id,
            SubCategory.sub_category_name,
            SubCategory.slug,
            SubCategory.sub_category_image,
            SubCategory.is_active,
            SubCategory.created_at,
        )
        .join(Category, Category.id == SubCategory.category_id)
        .filter(SubCategory.is_delete == False)
    )


def upload_sub_category_image(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise AppException(400, "Only JPG and PNG images allowed")

    contents = file.file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise AppException(400, "Image must be less than 1MB")

    result = cloudinary.uploader.upload(
        contents,
        folder="myvegiz/sub-categories",
        resource_type="image"
    )
    return result["secure_url"]


def generate_slug(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")


# =========================
# CREATE
# =========================
def create_sub_category(
    db: Session,
    data: SubCategoryCreate,
    image: UploadFile = None
):
    category = db.query(Category).filter(
        Category.id == data.category_id,
        Category.is_delete == False
    ).first()

    if not category:
        raise AppException(404, "Category not found")

    slug = generate_slug(data.sub_category_name)

    if db.query(SubCategory).filter(
        SubCategory.slug == slug,
        SubCategory.category_id == data.category_id,
        SubCategory.is_delete == False
    ).first():
        raise AppException(400, "Sub category already exists")

    image_url = upload_sub_category_image(image) if image and image.filename else None

    sub_category = SubCategory(
        uu_id=str(uuid.uuid4()),
        category_id=data.category_id,
        sub_category_name=data.sub_category_name,
        slug=slug,
        sub_category_image=image_url,
        is_active=data.is_active
    )

    try:
        db.add(sub_category)
        db.commit()
        db.refresh(sub_category)
        # return sub_category
        return (
        category_with_name_query(db)
        .filter(SubCategory.id == sub_category.id)
        .first()
    )
    except IntegrityError:
        db.rollback()
        raise AppException(500, "Database error")


# =========================
# LIST
# =========================
def list_sub_categories(db: Session, offset: int, limit: int):
    base_query = category_with_name_query(db).filter(
        # SubCategory.is_active == True
    ).order_by(SubCategory.created_at.desc())

    total_records = base_query.count()

    sub_categories = base_query.offset(offset).limit(limit).all()

    return total_records, sub_categories



# =========================
# UPDATE
# =========================
def update_sub_category(
    db: Session,
    uu_id: str,
    data: SubCategoryUpdate,
    image: UploadFile = None
):
    sub_category = db.query(SubCategory).filter(
        SubCategory.uu_id == uu_id,
        SubCategory.is_delete == False
    ).first()

    if not sub_category:
        raise AppException(404, "Sub category not found")

    if data.category_id:
        category = db.query(Category).filter(
            Category.id == data.category_id,
            Category.is_delete == False
        ).first()
        if not category:
            raise AppException(404, "Category not found")
        sub_category.category_id = data.category_id

    if data.sub_category_name:
        new_slug = generate_slug(data.sub_category_name)

        if db.query(SubCategory).filter(
            SubCategory.slug == new_slug,
            SubCategory.category_id == sub_category.category_id,
            SubCategory.uu_id != uu_id,
            SubCategory.is_delete == False
        ).first():
            raise AppException(400, "Sub category already exists")

        sub_category.sub_category_name = data.sub_category_name
        sub_category.slug = new_slug

    if data.is_active is not None:
        sub_category.is_active = data.is_active

    if image and image.filename:
        sub_category.sub_category_image = upload_sub_category_image(image)

    sub_category.is_update = True
    sub_category.updated_at = func.now()

    db.commit()
    db.refresh(sub_category)
    # return sub_category

    return (
        category_with_name_query(db)
        .filter(SubCategory.uu_id == uu_id)
        .first()
            )
# =========================
# DELETE (SOFT)
# =========================
def soft_delete_sub_category(db: Session, uu_id: str):
    sub_category = db.query(SubCategory).filter(
        SubCategory.uu_id == uu_id,
        SubCategory.is_delete == False
    ).first()

    if not sub_category:
        raise AppException(404, "Sub category not found")

    sub_category.is_delete = True
    sub_category.is_active = False
    sub_category.deleted_at = func.now()

    db.commit()
    db.refresh(sub_category)
    # return sub_category

    return (
            category_with_name_query(db)
            .filter(sub_category.uu_id == uu_id)
            .first()
        ) 




def get_category_dropdown(db: Session):
    return (
        db.query(Category)
        .filter(
            Category.is_active == True,
            Category.is_delete == False

        )
        .order_by(Category.category_name.asc())
        .all()
    )

