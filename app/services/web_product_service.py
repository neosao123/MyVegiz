from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session, joinedload
from app.models.product import Product


def list_web_products(
    db: Session,
    offset: int,
    limit: int,
    category_id: int = None,
    sub_category_id: int = None
):
    base_query = db.query(Product).options(
        joinedload(Product.images)
    ).filter(
        Product.is_delete == False,
        Product.is_active == True
    ).order_by(Product.created_at.desc())

    # Optional filters
    if category_id:
        base_query = base_query.filter(Product.category_id == category_id)

    if sub_category_id:
        base_query = base_query.filter(Product.sub_category_id == sub_category_id)

    total_records = base_query.count()
    data = base_query.offset(offset).limit(limit).all()

    return total_records, data


