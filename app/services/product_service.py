

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
    return result["secure_url"]


def generate_slug(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")


# ---------- CREATE ----------
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
            db.add(ProductImage(
                product_id=db_product.id,
                product_image=upload_product_image(image),
                is_primary=index == 0
            ))

        db.commit()
        product_with_images = db.query(Product).options(
            joinedload(Product.images)
        ).filter(Product.id == db_product.id).first()

        return product_with_images
    except IntegrityError as e:
        db.rollback()
        print("DB ERROR 👉", e.orig)   # 👈 THIS LINE

        raise AppException(status=500, message="Database error while creating product")




def list_products(db: Session, offset: int, limit: int):
    # -------------------------------
    # Base filters (soft delete aware)
    # -------------------------------
    base_query = db.query(Product).filter(
        Product.is_delete == False,
        Product.is_active == True
    ).order_by(Product.created_at.desc())

    total_records = base_query.count()

    products = base_query.offset(offset).limit(limit).all()

    return total_records, products


# ---------- UPDATE ----------
def update_product(
    db: Session,
    uu_id: str,
    data: ProductUpdate,
    images: list[UploadFile]
):
    product = db.query(Product).filter(
        Product.uu_id == uu_id,
        Product.is_delete == False
    ).first()

    if not product:
        raise AppException(status=404, message="Product not found")

     # ---------- CATEGORY UPDATE (OPTIONAL) ----------
    if data.category_id is not None:
        category = db.query(Category).filter(
            Category.id == data.category_id,
            Category.is_delete == False
        ).first()

        if not category:
            raise AppException(status=404, message="Category not found")

        product.category_id = data.category_id

      # ---------- SUB CATEGORY UPDATE (OPTIONAL) ----------
    if data.sub_category_id is not None:
        from app.models.sub_category import SubCategory

        sub_category = db.query(SubCategory).filter(
            SubCategory.id == data.sub_category_id,
            SubCategory.is_delete == False
        ).first()

        if not sub_category:
            raise AppException(status=404, message="Sub category not found")

        # 🔒 Ensure sub-category belongs to category
        if data.category_id and sub_category.category_id != data.category_id:
            raise AppException(
                status=400,
                message="Sub category does not belong to selected category"
            )

        product.sub_category_id = data.sub_category_id

    # 🔐 UPDATE ONLY PROVIDED FIELDS
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

    # 🖼️ OPTIONAL IMAGE UPDATE
    if images:
        with db.no_autoflush:
            db.query(ProductImage).filter(
                ProductImage.product_id == product.id
            ).delete()

        for index, image in enumerate(images):
            image_url = upload_product_image(image)
            db.add(ProductImage(
                product_id=product.id,
                product_image=image_url,
                is_primary=(index == 0)
            ))

    db.commit()


    return db.query(Product).options(
    joinedload(Product.images)
    ).filter(Product.id == product.id).first()



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

    #  SOFT DELETE RELATED IMAGES
    db.query(ProductImage).filter(
        ProductImage.product_id == product.id,
        ProductImage.is_delete == False
    ).update(
        {
            ProductImage.is_delete: True,
            ProductImage.is_active: False,
            ProductImage.deleted_at: func.now(),
            ProductImage.is_update: True
        },
        synchronize_session=False
    )

    db.commit()
    db.refresh(product)
    return product




def get_sub_category_dropdown(db: Session):
    return (
        db.query(SubCategory)
        .filter(
            SubCategory.is_active == True
        )
        .order_by(SubCategory.sub_category_name.asc())
        .all()
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