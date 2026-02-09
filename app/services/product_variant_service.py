from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
import uuid

from app.models.product_variants import ProductVariants
from app.models.product import Product
from app.models.uom import UOM
from app.models.zone import Zone
from app.schemas import product_variant
from app.schemas.product_variant import ProductVariantBulkCreate,VariantItem
from app.core.exceptions import AppException
from sqlalchemy.orm import joinedload



from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from app.core.search import apply_trigram_search


# ============================================================
# SEARCH FUNCTIONALITY
# ============================================================
def search_product_variants(
    db: Session,
    search: str,
    offset: int,
    limit: int
):
    query = (
        db.query(ProductVariants)
        .join(Product, Product.id == ProductVariants.product_id)
        .join(Zone, Zone.id == ProductVariants.zone_id)
        .join(UOM, UOM.id == ProductVariants.uom_id)
        .options(
            joinedload(ProductVariants.product),
            joinedload(ProductVariants.zone),
            joinedload(ProductVariants.uom)
        )
        .filter(
            ProductVariants.is_delete == False
        )
    )

    # Trigram-based search across related tables
    query = apply_trigram_search(
        query=query,
        search=search,
        fields=[
            Product.product_name,
            Zone.zone_name,
            UOM.uom_name
        ],
        order_fields=[
            Product.product_name,
            Zone.zone_name,
            UOM.uom_name
        ]
    )

    total = query.count()

    variants = (
        query
        .order_by(ProductVariants.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, variants


# ============================================================
# BULK CREATE PRODUCT VARIANTS
# ============================================================
def bulk_create_product_variants(
    db: Session,
    data: ProductVariantBulkCreate
):
    # -------------------------------
    # Validate Product
    # -------------------------------
    product = db.query(Product).filter(
        Product.id == data.product_id,
        Product.is_delete == False
    ).first()

    if not product:
        raise AppException(status=404, message="Product not found")

    variants_to_create = []

    for item in data.variants:

        # -------------------------------
        # VALIDATE QUANTITY
        # -------------------------------
        if item.quantity is None or item.quantity <= 0:
            raise AppException(
                status=400,
                message="Quantity must be greater than 0"
            )
    
        # -------------------------------
        # Validate Zone
        # -------------------------------
        if not db.query(Zone).filter(
            Zone.id == item.zone_id,
            Zone.is_delete == False
        ).first():
            raise AppException(
                status=404,
                message=f"Zone not found (ID: {item.zone_id})"
            )

        # -------------------------------
        # Validate UOM
        # -------------------------------
        if not db.query(UOM).filter(
            UOM.id == item.uom_id,
            UOM.is_delete == False
        ).first():
            raise AppException(
                status=404,
                message=f"UOM not found (ID: {item.uom_id})"
            )

        # -------------------------------
        # Prevent duplicate variants
        # -------------------------------
        exists = db.query(ProductVariants).filter(
            ProductVariants.product_id == data.product_id,
            ProductVariants.zone_id == item.zone_id,
            ProductVariants.uom_id == item.uom_id,
            ProductVariants.is_delete == False
        ).first()

        if exists:
            raise AppException(
                status=400,
                message=f"Variant already exists (zone={item.zone_id}, uom={item.uom_id})"
            )

        variants_to_create.append(
            ProductVariants(
                uu_id=str(uuid.uuid4()),
                product_id=data.product_id,
                zone_id=item.zone_id,
                uom_id=item.uom_id,
                quantity=item.quantity,
                actual_price=item.actual_price,
                selling_price=item.selling_price,
                is_deliverable=item.is_deliverable if item.is_deliverable is not None else True,
                is_active=True
            )
        )

    try:
        db.add_all(variants_to_create)
        db.commit()

        # Refresh each object to get ID & created_at
        for variant in variants_to_create:
            db.refresh(variant)

        return variants_to_create

    except IntegrityError:
        db.rollback()
        raise AppException(
            status=500,
            message="Database error while creating product variants"
        )


# ============================================================
# LIST ALL PRODUCT VARIANTS (PAGINATED)
# ============================================================
def list_all_product_variants(db: Session, offset: int, limit: int):
    # -------------------------------
    # Base filters (soft delete aware)
    # -------------------------------
    base_query = db.query(ProductVariants).options(
        joinedload(ProductVariants.product),
        joinedload(ProductVariants.uom),
        joinedload(ProductVariants.zone)
    ).filter(
        ProductVariants.is_delete == False,
        # ProductVariants.is_active == True
    ).order_by(ProductVariants.created_at.desc())

    total_records = base_query.count()

    product_variants = base_query.offset(offset).limit(limit).all()

    return total_records, product_variants


# ============================================================
# UPDATE PRODUCT VARIANT
# ============================================================
def update_product_variant(
    db: Session,
    uu_id: str,
    data: dict
):
    variant = db.query(ProductVariants).filter(
        ProductVariants.uu_id == uu_id,
        ProductVariants.is_delete == False
    ).first()

    if not variant:
        raise AppException(status=404, message="Variant not found")
    
    if "quantity" in data:
        if data["quantity"] is None or data["quantity"] <= 0:
            raise AppException(
                status=400,
                message="Quantity must be greater than 0"
            )
        variant.quantity = data["quantity"]

    if "actual_price" in data:
        variant.actual_price = data["actual_price"]

    if "selling_price" in data:
        variant.selling_price = data["selling_price"]

    if "is_active" in data:
        variant.is_active = data["is_active"]

    if "is_deliverable" in data:
        variant.is_deliverable = data["is_deliverable"]

    try:
        db.commit()
        db.refresh(variant)
        return variant
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Failed to update variant")


# ============================================================
# SOFT DELETE PRODUCT VARIANT
# ============================================================
def soft_delete_product_variant(
    db: Session,
    uu_id: str
):
    variant = db.query(ProductVariants).filter(
        ProductVariants.uu_id == uu_id,
        ProductVariants.is_delete == False
    ).first()

    if not variant:
        raise AppException(status=404, message="Variant not found")

    variant.is_delete = True
    variant.is_active = False
    variant.deleted_at = func.now()

    try:
        db.commit()
        db.refresh(variant)
        return variant
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Failed to delete variant")



# -------------------------
# ZONE DROPDOWN
# -------------------------
def list_zone_dropdown(db: Session):
    zones = db.query(Zone).filter(
        Zone.is_delete == False,
        Zone.is_active == True
    ).order_by(Zone.zone_name.asc()).all()

    return zones


# -------------------------
# UOM DROPDOWN
# -------------------------
def list_uom_dropdown(db: Session):
    uoms = db.query(UOM).filter(
        UOM.is_delete == False,
        UOM.is_active == True
    ).order_by(UOM.uom_name.asc()).all()

    return uoms


# -------------------------
# PRODUCT DROPDOWN
# -------------------------
def list_product_dropdown(db: Session):
    products = db.query(Product).filter(
        Product.is_delete == False,
        Product.is_active == True
    ).order_by(Product.product_name.asc()).all()

    return products
