from sqlalchemy.orm import Session
from app.models.product_variants import ProductVariants
from app.models.zone import Zone
from app.utils.geo import point_in_polygon



from sqlalchemy.orm import Session, joinedload
from app.models.product import Product
from app.models.uom import UOM
from app.models.category import Category
from app.models.sub_category import SubCategory
from app.models.main_category import MainCategory


def product_variant_with_product_uom_query(db: Session):
    return (
        db.query(ProductVariants)
        .join(Product, Product.id == ProductVariants.product_id)
        .join(Category, Category.id == Product.category_id)
        .join(MainCategory, MainCategory.id == Category.main_category_id)
        .join(UOM, UOM.id == ProductVariants.uom_id)
        .options(
            joinedload(ProductVariants.product)
                .joinedload(Product.category)
                .joinedload(Category.main_category),
            joinedload(ProductVariants.product)
                .joinedload(Product.sub_category),
            joinedload(ProductVariants.product)
                .joinedload(Product.images),
            joinedload(ProductVariants.uom),
        )
    )




def list_all_product_variants(
    db: Session,
    lat: float,
    lng: float,
    offset: int,
    limit: int,
    main_category_slug: str | None = None,
):
    # ----------------------------------
    # 1. Find zones that contain the point
    # ----------------------------------
    zones = db.query(Zone).filter(
        Zone.is_delete == False,
        Zone.is_active == True
    ).all()

    matching_zones = [
        z for z in zones
        if point_in_polygon(lat, lng, z.polygon)
    ]

    # Check if point is in any zone
    if not matching_zones:
        return None, None, "Location is outside our service area"

    # Check if any matching zone is deliverable
    deliverable_zone_ids = [z.id for z in matching_zones if z.is_deliverable]
    
    if not deliverable_zone_ids:
        return None, None, "Delivery is not available in this area"

    # ----------------------------------
    # 2. Product Variants + Product + UOM
    # ----------------------------------
    base_query = (
        product_variant_with_product_uom_query(db)
        .filter(
            ProductVariants.zone_id.in_(deliverable_zone_ids),
            ProductVariants.is_delete == False,
            ProductVariants.is_active == True
        )
        .order_by(ProductVariants.created_at.desc())
    )

    if main_category_slug:   # MAIN CATEGORY FILTER
        base_query = base_query.filter(
            MainCategory.slug == main_category_slug
        )

    base_query = base_query.order_by(ProductVariants.created_at.desc())

    total_records = base_query.count()

    variants = (
        base_query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total_records, variants, None