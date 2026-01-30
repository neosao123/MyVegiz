from sqlalchemy.orm import Session
from app.models.category import Category


def list_web_categories(
    db: Session,
    offset: int,
    limit: int
):
    base_query = db.query(Category).filter(
        Category.is_active == True,
        Category.is_delete == False
    ).order_by(Category.created_at.desc())

    total_records = base_query.count()
    data = base_query.offset(offset).limit(limit).all()

    return total_records, data
