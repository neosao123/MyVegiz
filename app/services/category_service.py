from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import UploadFile
from sqlalchemy.sql import func
import uuid
import re

from app.models.category import Category
from app.schemas.category import CategoryCreate,CategoryUpdate
from app.core.exceptions import AppException
import cloudinary.uploader
from app.models.main_category import MainCategory



MAX_IMAGE_SIZE = 1 * 1024 * 1024  # 1MB
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]


# =========================================================
# BASE QUERY (CATEGORY + MAIN CATEGORY NAME)
# Used for list & response formatting
# =========================================================
def category_with_main_name_query(db):
    return (
        db.query(
            Category.id,
            Category.main_category_id,
            MainCategory.main_category_name.label("main_category_name"),
            Category.uu_id,
            Category.category_name,
            Category.slug,
            Category.category_image,
            Category.is_active,
            Category.created_at,
        )
        .join(MainCategory, MainCategory.id == Category.main_category_id)
        .filter(Category.is_delete == False)
    )

# =========================================================
# IMAGE UPLOAD (CLOUDINARY)
# =========================================================
def upload_category_image(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise AppException(status=400, message="Only JPG and PNG images are allowed")

    contents = file.file.read()

    if len(contents) > MAX_IMAGE_SIZE:
        raise AppException(status=400, message="Category image must be less than 1 MB")

    result = cloudinary.uploader.upload(
        contents,
        folder="myvegiz/categories",
        resource_type="image"
    )

    return result["secure_url"]


# =========================================================
# SLUG GENERATOR
# =========================================================
def generate_slug(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")
    return slug



# =========================================================
# CREATE CATEGORY
# =========================================================
def create_category(
    db: Session,
    category: CategoryCreate,
    category_image: UploadFile = None
):
    if not category_image:
        raise AppException(status=400, message="Category image is required")

    # Validate main category
    main_category = db.query(MainCategory).filter(
        MainCategory.id == category.main_category_id,
    ).first()

    
    if not main_category:
        raise AppException(status=404, message="Main category not found")



    # Generate UUID & Slug
    uu_id = str(uuid.uuid4())
    slug = generate_slug(category.category_name)

    # Check slug uniqueness
    slug_exists = db.query(Category).filter(
        Category.slug == slug,
        Category.is_delete == False
    ).first()

    if slug_exists:
        raise AppException(status=400, message="Category already exists")

    image_url = None
    if category_image:
        image_url = upload_category_image(category_image)

    db_category = Category(
        uu_id=uu_id,
        main_category_id=category.main_category_id,  
        category_name=category.category_name,
        slug=slug,
        category_image=image_url,
        is_active=category.is_active
    )

    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return (
        category_with_main_name_query(db)
        .filter(Category.id == db_category.id)
        .first()
    )
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error while creating category")


# =========================================================
# LIST CATEGORIES (PAGINATED)
# =========================================================
def list_categories(db: Session, offset: int, limit: int):
    # -------------------------------
    # Base filters (soft delete aware)
    # -------------------------------
    base_query =category_with_main_name_query(db).filter(
        # Category.is_active == True
    ).order_by(Category.created_at.desc())

    total_records = base_query.count()

    categories = base_query.offset(offset).limit(limit).all()

    return total_records, categories




def generate_slug(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")


# =========================================================
# UPDATE CATEGORY
# =========================================================
def update_category(
    db: Session,
    uu_id: str,
    category_data: CategoryUpdate,
    category_image: UploadFile = None
):
    category = db.query(Category).filter(
        Category.uu_id == uu_id,
        Category.is_delete == False
    ).first()

    if not category:
        raise AppException(status=404, message="Category not found")

    #  Update main category if provided
    if category_data.main_category_id is not None:
        main_category = db.query(MainCategory).filter(
            MainCategory.id == category_data.main_category_id,
        ).first()

        if not main_category:
            raise AppException(status=404, message="Main category not found")

        category.main_category_id = category_data.main_category_id


    # ---------- NAME + SLUG ----------
    if category_data.category_name is not None:
        new_slug = generate_slug(category_data.category_name)

        slug_exists = db.query(Category).filter(
            Category.slug == new_slug,
            Category.is_delete == False,
            Category.uu_id != uu_id 
        ).first()

        if slug_exists:
            raise AppException(status=400, message="Category already exists")

        category.category_name = category_data.category_name
        category.slug = new_slug

    # ---------- ACTIVE ----------
    if category_data.is_active is not None:
        category.is_active = category_data.is_active

    # ---------- IMAGE ----------
    if category_image:
        category.category_image = upload_category_image(category_image)

    category.is_update = True
    category.updated_at = func.now()

    try:
        db.commit()
        db.refresh(category)
        
        return (
            category_with_main_name_query(db)
            .filter(Category.uu_id == uu_id)
            .first()
        )
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error while updating category")




# =========================================================
# SOFT DELETE CATEGORY
# =========================================================
def soft_delete_category(db: Session, uu_id: str):
    category = db.query(Category).filter(
        Category.uu_id == uu_id,
        Category.is_delete == False
    ).first()

    if not category:
        raise AppException(status=404, message="Category not found")

 
    category.is_delete = True
    category.is_active = False
    category.deleted_at = func.now()

    try:
        db.commit()
        db.refresh(category)

        return (
            category_with_main_name_query(db)
            .filter(Category.uu_id == uu_id)
            .first()
        ) 
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error while deleting category")



# =========================================================
# MAIN CATEGORY DROPDOWN
# =========================================================
def get_main_category_dropdown(db: Session):
    return (
        db.query(MainCategory)
        .filter(
            MainCategory.is_active == True
        )
        .order_by(MainCategory.main_category_name.asc())
        .all()
    )



