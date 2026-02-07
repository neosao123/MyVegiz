from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
import uuid
import re

from app.models.uom import UOM
from app.schemas.uom import UOMCreate, UOMUpdate
from app.core.exceptions import AppException


from app.core.search import apply_trigram_search


# ============================================================
# SEARCH FUNCTIONALITY
# ============================================================
def search_uoms(
    db: Session,
    search: str,
    offset: int,
    limit: int
):
    query = (
        db.query(UOM)
        .filter(
            UOM.is_delete == False
        )
    )

    # 🔍 Trigram similarity search
    query = apply_trigram_search(
        query=query,
        search=search,
        fields=[
            UOM.uom_name,
            UOM.uom_code,
            UOM.uom_short_name,
            UOM.description
        ],
        order_fields=[
            UOM.uom_name,
            UOM.uom_code,
            UOM.uom_short_name
        ]
    )

    total = query.count()

    uoms = (
        query
        .order_by(UOM.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, uoms



# ============================================================
# UOM CODE GENERATOR
# ============================================================
def generate_uom_code(name: str) -> str:
    base = re.sub(r"[^A-Za-z0-9]+", "-", name.lower()).strip("-")
    return f"{base}-{uuid.uuid4().hex[:6]}"


# ============================================================
# CREATE UOM
# ============================================================
def create_uom(db: Session, uom: UOMCreate):

    # ---- NAME UNIQUE ----
    name_exists = db.query(UOM).filter(
        UOM.uom_name == uom.uom_name,
        UOM.is_delete == False
    ).first()

    if name_exists:
        raise AppException(status=400, message="UOM name already exists")
    

    # ---- SHORT NAME UNIQUE ----
    short_exists = db.query(UOM).filter(
        UOM.uom_short_name == uom.uom_short_name,
        UOM.is_delete == False
    ).first()

    if short_exists:
        raise AppException(status=400, message="UOM short name already exists")
    

    uom_code = generate_uom_code(uom.uom_name)


    db_uom = UOM(
        uu_id=str(uuid.uuid4()),
        uom_code=uom_code,
        uom_name=uom.uom_name,
        uom_short_name=uom.uom_short_name,
        description=uom.description,
        is_active=uom.is_active
    )

    try:
        db.add(db_uom)
        db.commit()
        db.refresh(db_uom)
        return db_uom
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error while creating UOM")


# ============================================================
# LIST UOMS
# ============================================================
def list_uoms(db: Session, offset: int, limit: int):
    # -------------------------------
    # Base filters (soft delete aware)
    # -------------------------------
    base_query = db.query(UOM).filter(
        UOM.is_delete == False,
    ).order_by(UOM.created_at.desc())

    total_records = base_query.count()

    uoms = base_query.offset(offset).limit(limit).all()

    return total_records, uoms

# ============================================================
# UPDATE UOM
# ============================================================
def update_uom(db: Session, uu_id: str, data: UOMUpdate):
    uom = db.query(UOM).filter(
        UOM.uu_id  == uu_id ,
        UOM.is_delete == False
    ).first()

    if not uom:
        raise AppException(status=404, message="UOM not found")
    


    # ---- NAME UNIQUE ----
    if data.uom_name:
        name_exists = db.query(UOM).filter(
            UOM.uom_name == data.uom_name,
            UOM.uu_id  != uu_id ,
            UOM.is_delete == False
        ).first()

        if name_exists:
            raise AppException(status=400, message="UOM name already exists")

        uom.uom_name = data.uom_name


    # ---- SHORT NAME UNIQUE ----
    if data.uom_short_name:
        short_exists = db.query(UOM).filter(
            UOM.uom_short_name == data.uom_short_name,
            UOM.uu_id  != uu_id ,
            UOM.is_delete == False
        ).first()

        if short_exists:
            raise AppException(status=400, message="UOM short name already exists")

        uom.uom_short_name = data.uom_short_name


    if data.description is not None:
        uom.description = data.description

    if data.is_active is not None:
        uom.is_active = data.is_active

    uom.is_update = True
    uom.updated_at = func.now()

    try:
        db.commit()
        db.refresh(uom)
        return uom
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error while updating UOM")


# ============================================================
# SOFT DELETE UOM
# ============================================================
def soft_delete_uom(db: Session, uu_id: str):
    uom = db.query(UOM).filter(
        UOM.uu_id  == uu_id ,
        UOM.is_delete == False
    ).first()

    if not uom:
        raise AppException(status=404, message="UOM not found")

    uom.is_delete = True
    uom.is_active = False
    uom.deleted_at = func.now()

    try:
        db.commit()
        db.refresh(uom)
        return uom
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error while deleting UOM")
