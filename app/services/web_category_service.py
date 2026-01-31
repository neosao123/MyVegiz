from sqlalchemy.orm import Session
from app.models.category import Category

from app.models.main_category import MainCategory



def web_category_with_main_name_query(db: Session):
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
        .join(
            MainCategory,
            MainCategory.id == Category.main_category_id
        )
        .filter(
            Category.is_delete == False,
            Category.is_active == True
        )
    )



def list_web_categories(
    db: Session,
    offset: int,
    limit: int,
    main_category_id: int | None = None
):
    base_query = web_category_with_main_name_query(db)

    # OPTIONAL FILTER
    if main_category_id is not None:
        base_query = base_query.filter(
            Category.main_category_id == main_category_id
        )

    base_query = base_query.order_by(Category.created_at.desc())

    total_records = base_query.count()
    data = base_query.offset(offset).limit(limit).all()

    return total_records, data
