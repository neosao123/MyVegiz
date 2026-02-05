from itertools import product
import uuid
import re
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from app.models.sub_category import SubCategory
from fastapi import UploadFile

from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate
from app.core.exceptions import AppException
import cloudinary.uploader
from sqlalchemy.orm import joinedload

MAX_IMAGE_SIZE = 1 * 1024 * 1024
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]

# =========================================================
# IMAGE UPLOAD HANDLER
# =========================================================
def upload_product_image(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise AppException(status=400, message="Only JPG and PNG images are allowed")

    content = file.file.read()
    if len(content) > MAX_IMAGE_SIZE:
        raise AppException(status=400, message="Product image must be less than 1 MB")

    result = cloudinary.uploader.upload(
        content,
        folder="myvegiz/products",
        resource_type="image"
    )

    return {
        "url": result["secure_url"],
        "public_id": result["public_id"]
    }

# =========================================================
# SLUG GENERATOR
# =========================================================
def generate_slug(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")


# =========================================================
# CREATE PRODUCT
# =========================================================
def create_product(
    db: Session,
    product: ProductCreate,
    images: list[UploadFile]
):
    category = db.query(Category).filter(
        Category.id == product.category_id,
        Category.is_delete == False
    ).first()

    if not category:
        raise AppException(status=404, message="Category not found")

    #  Sub-category OPTIONAL
    if product.sub_category_id is not None:
        from app.models.sub_category import SubCategory

        sub_category = db.query(SubCategory).filter(
            SubCategory.id == product.sub_category_id,
            SubCategory.is_delete == False
        ).first()

        if not sub_category:
            raise AppException(status=404, message="Sub category not found")

    uu_id = str(uuid.uuid4())
    slug = generate_slug(product.product_name)

    if db.query(Product).filter(Product.slug == slug, Product.is_delete == False).first():
        raise AppException(status=400, message="Product already exists")

    db_product = Product(
        uu_id=uu_id,
        category_id=product.category_id,
        sub_category_id=product.sub_category_id,
        product_name=product.product_name,
        product_short_name=product.product_short_name,
        slug=slug,
        short_description=product.short_description,
        long_description=product.long_description,
        hsn_code=product.hsn_code,
        sku_code=product.sku_code,
        is_active=product.is_active
    )

    try:
        db.add(db_product)
        db.flush()

        for index, image in enumerate(images or []):
            upload = upload_product_image(image)

            db.add(ProductImage(
                product_id=db_product.id,
                product_image=upload["url"],
                public_id=upload["public_id"],
                is_primary=(index == 0)
            ))


        db.commit()
    
        return db.query(Product).options(joinedload(Product.images))\
        .filter(Product.id == db_product.id).first()
    except IntegrityError as e:
        db.rollback()
        print("DB ERROR 👉", e.orig)   # 👈 THIS LINE

        raise AppException(status=500, message="Database error while creating product")



# =========================================================
# LIST PRODUCTS (PAGINATED)
# =========================================================
def list_products(db: Session, offset: int, limit: int):
    # -------------------------------
    # Base filters (soft delete aware)
    # -------------------------------
    base_query = db.query(Product).filter(
        Product.is_delete == False,
        # Product.is_active == True
    ).order_by(Product.created_at.desc())

    total_records = base_query.count()

    products = base_query.offset(offset).limit(limit).all()

    return total_records, products


# =========================================================
# UPDATE PRODUCT
# =========================================================
def update_product(
    db: Session,
    uu_id: str,
    data: ProductUpdate,
    removed_image_ids: list[int],
    images: list[UploadFile]
):
    product = db.query(Product).filter(
        Product.uu_id == uu_id,
        Product.is_delete == False
    ).first()

    if not product:
        raise AppException(status=404, message="Product not found")


    # ---------------- UPDATE PRODUCT FIELDS ----------------
    if data.category_id is not None:
        product.category_id = data.category_id

    if data.sub_category_id is not None:
        product.sub_category_id = data.sub_category_id

    if data.product_name is not None:
        product.product_name = data.product_name
        product.slug = generate_slug(data.product_name)

    if data.product_short_name is not None:
        product.product_short_name = data.product_short_name

    if data.short_description is not None:
        product.short_description = data.short_description

    if data.long_description is not None:
        product.long_description = data.long_description

    if data.hsn_code is not None:
        product.hsn_code = data.hsn_code

    if data.sku_code is not None:
        product.sku_code = data.sku_code

    if data.is_active is not None:
        product.is_active = data.is_active

    product.is_update = True
    product.updated_at = func.now()

    # Count existing images BEFORE deletion
    existing_count = db.query(ProductImage).filter(
        ProductImage.product_id == product.id,
    ).count()

    # Compute total images after update
    total_images_after = existing_count - len(removed_image_ids or []) + len(images or [])

    # Validation
    if total_images_after == 0:
        raise AppException(status=400, message="At least 1 product image is required")
    if total_images_after > 5:
        raise AppException(status=400, message="Maximum 5 images are allowed")


    # ---------------- HARD DELETE IMAGES ----------------
    if removed_image_ids:
        imgs = db.query(ProductImage).filter(
            ProductImage.id.in_(removed_image_ids),
            ProductImage.product_id == product.id
        ).all()

        for img in imgs:
            if img.public_id:
                cloudinary.uploader.destroy(img.public_id)
            db.delete(img)

        db.flush()


    # ---------------- ADD NEW IMAGES ----------------
    if images:
        for image in images:
            upload = upload_product_image(image)
            db.add(ProductImage(
                product_id=product.id,
                product_image=upload["url"],
                public_id=upload["public_id"],
                is_primary=False
            ))

    db.flush()

    # ---------------- ENSURE ONE PRIMARY ----------------
    primary = db.query(ProductImage).filter(
        ProductImage.product_id == product.id,
        ProductImage.is_primary == True
    ).first()

    if not primary:
        first_img = db.query(ProductImage).filter(
            ProductImage.product_id == product.id
        ).order_by(ProductImage.created_at.asc()).first()
        if first_img:
            first_img.is_primary = True


    db.commit()
    db.refresh(product)

    return db.query(Product).options(
        joinedload(Product.images),
        joinedload(Product.category),
        joinedload(Product.sub_category)
    ).filter(Product.id == product.id).first()



# =========================================================
# SOFT DELETE PRODUCT
# =========================================================
def soft_delete_product(db: Session, uu_id: str):
    product = db.query(Product).filter(
        Product.uu_id == uu_id,
        Product.is_delete == False
    ).first()

    if not product:
        raise AppException(status=404, message="Product not found")

    #  SOFT DELETE PRODUCT
    product.is_delete = True
    product.is_active = False
    product.deleted_at = func.now()

        # 2️⃣ Fetch all related product images
    images = db.query(ProductImage).filter(
        ProductImage.product_id == product.id,
    ).all()

        # 3️⃣ Hard delete images from Cloudinary and DB
    for img in images:
        if img.public_id:
            try:
                cloudinary.uploader.destroy(img.public_id)
            except Exception as e:
                print("Cloudinary deletion error:", e)
        # Delete from DB
        db.delete(img)


    db.commit()
    db.refresh(product)
    return product


# =========================================================
# CATEGORY DROPDOWN
# =========================================================
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



# =========================================================
# SUB-CATEGORY DROPDOWN (BY CATEGORY UUID)
# =========================================================
def get_sub_category_dropdown_by_category_uu_id(
    db: Session,
    category_uu_id: str
):
    # 1️. Find category by uu_id
    category = db.query(Category).filter(
        Category.uu_id == category_uu_id,
        Category.is_delete == False,
        Category.is_active == True
    ).first()

    if not category:
        raise AppException(status=404, message="Category not found")

    # 2️. Fetch sub-categories by category_id
    return (
        db.query(
            SubCategory.id,
            SubCategory.category_id,
            SubCategory.sub_category_name
        )
        .filter(
            SubCategory.category_id == category.id,
            SubCategory.is_active == True,
            SubCategory.is_delete == False
        )
        .order_by(SubCategory.sub_category_name.asc())
        .all()
    )