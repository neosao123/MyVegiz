from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.schemas.coupon_code import CouponCodeCreate
from app.schemas.response import APIResponse
from app.services.coupon_code_service import create_coupon_code
from app.models.user import User
from app.schemas.coupon_code import CouponCodeResponse

from fastapi import Query
import math
from typing import List

from app.schemas.response import PaginatedAPIResponse
from app.services.coupon_code_service import get_coupon_codes_paginated

from app.schemas.coupon_code import CouponCodeUpdate
from app.services.coupon_code_service import update_coupon_code

from app.services.coupon_code_service import soft_delete_coupon_code



router = APIRouter()


@router.post("/create", response_model=APIResponse[CouponCodeResponse])
def create_api(
    data: CouponCodeCreate = Depends(CouponCodeCreate.as_form),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    coupon = create_coupon_code(db, data)
    return {
        "status": 201,
        "message": "Coupon created successfully",
        "data": coupon
    }



@router.get("/list", response_model=PaginatedAPIResponse[List[CouponCodeResponse]])
def list_coupon_codes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:

        offset = (page - 1) * limit

        coupons, total_records = get_coupon_codes_paginated(
            db=db,
            offset=offset,
            limit=limit
        )

        total_pages = math.ceil(total_records / limit) if limit else 1

        pagination = {
            "total": total_records,
            "per_page": limit,
            "current_page": page,
            "total_pages": total_pages,
        }

        if coupons:
            return {
                "status": 200,
                "message": "Coupon codes fetched successfully",
                "data": coupons,
                "pagination": pagination
            }

        return {
            "status": 300,
            "message": "No coupon codes found",
            "data": [],
            "pagination": pagination
        }

    except Exception:
        return {
            "status": 500,
            "message": "Failed to fetch coupon codes ",
            "data": [],
        }



@router.put("/update", response_model=APIResponse[CouponCodeResponse])
def update_coupon_api(
    uu_id: str,
    data: CouponCodeUpdate = Depends(CouponCodeUpdate.as_form),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    coupon = update_coupon_code(db, uu_id, data)

    return {
        "status": 200,
        "message": "Coupon code updated successfully",
        "data": coupon
    }



@router.delete("/delete", response_model=APIResponse[CouponCodeResponse])
def delete_coupon_code_api(
    uu_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted_coupon = soft_delete_coupon_code(db, uu_id)

    return {
        "status": 200,
        "message": "Coupon code deleted successfully",
        "data": deleted_coupon
    }
