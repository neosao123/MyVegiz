from sqlalchemy.orm import Session
from app.models.product_variants import ProductVariants
from app.models.zone import Zone
from app.utils.geo import point_in_polygon



from sqlalchemy.orm import Session, joinedload
from app.models.product import Product
from app.models.uom import UOM


def product_variant_with_product_uom_query(db: Session):
    return (
        db.query(ProductVariants)
        .join(Product, Product.id == ProductVariants.product_id)
        .join(UOM, UOM.id == ProductVariants.uom_id)
        .options(
            joinedload(ProductVariants.product),
            joinedload(ProductVariants.uom)
        )
    )


def list_all_product_variants(
    db: Session,
    lat: float,
    lng: float,
    offset: int,
    limit: int,
):
    # ----------------------------------
    # 1. Geo filter (same as now)
    # ----------------------------------
    zones = db.query(Zone).filter(
        Zone.is_delete == False,
        Zone.is_active == True,
        Zone.is_deliverable == True
    ).all()

    valid_zone_ids = [
        z.id for z in zones
        if point_in_polygon(lat, lng, z.polygon)
    ]

    if not valid_zone_ids:
        return 0, []

    # ----------------------------------
    # 2. Product Variants + Product + UOM
    # ----------------------------------
    base_query = (
        product_variant_with_product_uom_query(db)
        .filter(
            ProductVariants.zone_id.in_(valid_zone_ids),
            ProductVariants.is_delete == False,
            ProductVariants.is_active == True
        )
        .order_by(ProductVariants.created_at.desc())
    )

    total_records = base_query.count()

    variants = (
        base_query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total_records, variants

