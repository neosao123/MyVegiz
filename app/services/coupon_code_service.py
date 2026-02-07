from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid

from app.models.coupon_code import CouponCode
from app.schemas.coupon_code import CouponCodeCreate,CouponCodeUpdate
from app.core.exceptions import AppException

from sqlalchemy.sql import func

from app.core.search import apply_trigram_search


# =========================================================
# SEARCH FUNCTIOANLITY
# =========================================================
def search_coupon_codes(
    db: Session,
    search: str,
    offset: int,
    limit: int
):
    query = (
        db.query(CouponCode)
        .filter(
            CouponCode.is_delete == False
        )
    )

    # 🔍 Search by coupon_code & coupon_type
    query = apply_trigram_search(
        query=query,
        search=search,
        fields=[
            CouponCode.coupon_code,
            CouponCode.coupon_type
        ],
        order_fields=[
            CouponCode.coupon_code,
            CouponCode.coupon_type
        ]
    )

    total = query.count()

    coupons = (
        query
        .order_by(CouponCode.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return coupons, total



# =========================================================
# CREATE COUPON CODE
# =========================================================
def create_coupon_code(db: Session, data: CouponCodeCreate):

    # Duplicate coupon
    if db.query(CouponCode).filter(
        CouponCode.coupon_code == data.coupon_code,
        CouponCode.is_delete == False
    ).first():
        raise AppException(400, "Coupon code already exists")

    coupon = CouponCode(
        uu_id=str(uuid.uuid4()),
        coupon_code=data.coupon_code,
        coupon_type=data.coupon_type,
        disc_value=data.disc_value,
        cap_limit=data.cap_limit,
        order_value=data.order_value,
        termscondition=data.termscondition,
        coupon_description=data.coupon_description,
        use_limit=data.use_limit,
        expiry_date=data.expiry_date,
        is_active=data.is_active
    )

    try:
        db.add(coupon)
        db.commit()
        db.refresh(coupon)
        return coupon
    except IntegrityError:
        db.rollback()
        raise AppException(500, "Database error")

# =========================================================
# LIST COUPON CODES (PAGINATED)
# =========================================================
def get_coupon_codes_paginated(
    db: Session,
    offset: int,
    limit: int
):
    base_query = db.query(CouponCode).filter(
        CouponCode.is_delete == False,
        # CouponCode.is_active == True
    ).order_by(CouponCode.created_at.desc())

    total_records = base_query.count()

    coupons = base_query.offset(offset).limit(limit).all()

    return coupons, total_records



# =========================================================
# UPDATE COUPON CODE
# =========================================================
def update_coupon_code(
    db: Session,
    uu_id: str,
    data: CouponCodeUpdate
):
    coupon = db.query(CouponCode).filter(
        CouponCode.uu_id == uu_id,
        CouponCode.is_delete == False
    ).first()

    if not coupon:
        raise AppException(404, "Coupon code not found")

    # ---------- UNIQUE COUPON CODE ----------
    if data.coupon_code:
        exists = db.query(CouponCode).filter(
            CouponCode.coupon_code == data.coupon_code,
            CouponCode.is_delete == False,
            CouponCode.id != coupon.id
        ).first()

        if exists:
            raise AppException(400, "Coupon code already exists")

        coupon.coupon_code = data.coupon_code

    # ---------- APPLY FIELDS ----------
    update_fields = [
        "coupon_type", "disc_value", "cap_limit", "order_value",
        "termscondition", "coupon_description",
        "use_limit", "expiry_date", "is_active"
    ]

    for field in update_fields:
        value = getattr(data, field)
        if value is not None:
            setattr(coupon, field, value)

    coupon.is_update = True
    coupon.updated_at = func.now()

    try:
        db.commit()
        db.refresh(coupon)
        return coupon
    except IntegrityError:
        db.rollback()
        raise AppException(500, "Database error while updating coupon")



# =========================================================
# SOFT DELETE COUPON CODE
# =========================================================
def soft_delete_coupon_code(db: Session, uu_id: str):
    coupon = db.query(CouponCode).filter(
        CouponCode.uu_id == uu_id,
        CouponCode.is_delete == False
    ).first()

    if not coupon:
        raise AppException(404, "Coupon code not found")

    coupon.is_delete = True
    coupon.is_active = False
    coupon.deleted_at = func.now()

    try:
        db.commit()
        db.refresh(coupon)
        return coupon
    except IntegrityError:
        db.rollback()
        raise AppException(500, "Database error while deleting coupon code")


