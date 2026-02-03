# app/services/restaurant_entity_category_service.py
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import uuid

from app.models.entity_category import EntityCategory
from app.schemas.restaurant_entity_category import EntityCategoryCreate,EntityCategoryUpdate
from app.core.exceptions import AppException


def generate_entity_category_code(db: Session) -> str:
    last = (
        db.query(EntityCategory)
        .order_by(EntityCategory.id.desc())
        .first()
    )

    next_id = last.id + 1 if last else 1
    return f"ECAT_{next_id}"


def create_entity_category(
    db: Session,
    data: EntityCategoryCreate
):
    # Check duplicate name under same main category
    exists = db.query(EntityCategory).filter(
        EntityCategory.entity_category == data.entity_category,
        EntityCategory.main_category_id == data.main_category_id,
        EntityCategory.is_delete == False
    ).first()

    if exists:
        raise AppException(400, "Entity category already exists")

    entity = EntityCategory(
        uu_id=str(uuid.uuid4()),
        code=generate_entity_category_code(db),
        entity_category=data.entity_category,
        main_category_id=data.main_category_id or 17,
        is_active=data.is_active
    )

    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity



def list_entity_categories(
    db: Session,
    offset: int,
    limit: int,
    main_category_id: int | None = None
):
    base_query = db.query(EntityCategory).filter(
        EntityCategory.is_delete == False
    ).order_by(EntityCategory.created_at.desc())

    # Optional filter by main_category
    if main_category_id:
        base_query = base_query.filter(
            EntityCategory.main_category_id == main_category_id
        )

    total_records = base_query.count()
    data = base_query.offset(offset).limit(limit).all()

    return total_records, data




def update_entity_category(
    db: Session,
    uu_id: str,
    data: EntityCategoryUpdate
):
    entity = db.query(EntityCategory).filter(
        EntityCategory.uu_id == uu_id,
        EntityCategory.is_delete == False
    ).first()

    if not entity:
        raise AppException(404, "Entity category not found")

    # Update entity_category (with duplicate check)
    if data.entity_category:
        exists = db.query(EntityCategory).filter(
            EntityCategory.entity_category == data.entity_category,
            EntityCategory.main_category_id == entity.main_category_id,
            EntityCategory.uu_id != uu_id,
            EntityCategory.is_delete == False
        ).first()

        if exists:
            raise AppException(400, "Entity category already exists")

        entity.entity_category = data.entity_category

    # Update active flag
    if data.is_active is not None:
        entity.is_active = data.is_active

    entity.is_update = True
    entity.updated_at = func.now()

    db.commit()
    db.refresh(entity)
    return entity



def delete_entity_category(
    db: Session,
    uu_id: str
):
    entity = db.query(EntityCategory).filter(
        EntityCategory.uu_id == uu_id,
        EntityCategory.is_delete == False
    ).first()

    if not entity:
        raise AppException(404, "Entity category not found")

    entity.is_delete = True
    entity.is_active = False
    entity.deleted_at = func.now()
    entity.updated_at = func.now()

    db.commit()
    db.refresh(entity)
    return entity

