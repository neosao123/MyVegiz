from sqlalchemy.orm import Session
from app.models.product_variants import ProductVariants
from app.models.zone import Zone
from app.utils.geo import point_in_polygon


def list_all_product_variants(
    db: Session,
    lat: float,
    lng: float,
    offset: int,
    limit: int,
):
    # ----------------------------------
    # 1. Fetch valid zones by geo filter
    # ----------------------------------
    zones = db.query(Zone).filter(
        Zone.is_delete == False,
        Zone.is_active == True,
        Zone.is_deliverable == True
    ).all()

    valid_zone_ids: list[int] = []

    for zone in zones:
        if point_in_polygon(lat, lng, zone.polygon):
            valid_zone_ids.append(zone.id)

    if not valid_zone_ids:
        return 0, []

    # ----------------------------------
    # 2. Fetch product variants
    # ----------------------------------
    base_query = db.query(ProductVariants).filter(
        ProductVariants.zone_id.in_(valid_zone_ids),
        ProductVariants.is_delete == False,
        ProductVariants.is_active == True
        # ProductVariants.is_deliverable == True
    ).order_by(ProductVariants.created_at.desc())

    total_records = base_query.count()

    product_variants = (
        base_query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total_records, product_variants
