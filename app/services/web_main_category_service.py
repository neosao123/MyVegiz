from sqlalchemy.orm import Session
from app.models.main_category import MainCategory


def list_web_main_categories(db: Session, offset: int, limit: int):
    base_query = db.query(MainCategory).filter(
        MainCategory.is_active == True
    ).order_by(MainCategory.created_at.desc())

    total_records = base_query.count()
    data = base_query.offset(offset).limit(limit).all()

    return total_records, data
