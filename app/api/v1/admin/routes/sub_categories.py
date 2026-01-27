from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
import math
from typing import List

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.sub_category import (
    SubCategoryCreate,
    SubCategoryUpdate,
    SubCategoryResponse
)
from app.schemas.response import APIResponse, PaginatedAPIResponse
from app.services.sub_category_service import (
    create_sub_category,
    list_sub_categories,
    update_sub_category,
    soft_delete_sub_category
)

router = APIRouter()


@router.post("/create", response_model=APIResponse[SubCategoryResponse])
def create_api(
    data: SubCategoryCreate = Depends(SubCategoryCreate.as_form),
    sub_category_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    sub_category = create_sub_category(db, data, sub_category_image)
    return {"status": 201, "message": "Created successfully", "data": sub_category}


@router.get("/list", response_model=PaginatedAPIResponse[List[SubCategoryResponse]])
def list_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    offset = (page - 1) * limit
    total, data = list_sub_categories(db, offset, limit)

    return {
        "status": 200,
        "message": "Fetched successfully",
        "data": data,
        "pagination": {
            "total": total,
            "per_page": limit,
            "current_page": page,
            "total_pages": math.ceil(total / limit)
        }
    }


@router.put("/update", response_model=APIResponse[SubCategoryResponse])
def update_api(
    uu_id: str,
    data: SubCategoryUpdate = Depends(SubCategoryUpdate.as_form),
    sub_category_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    sub_category = update_sub_category(db, uu_id, data, sub_category_image)
    return {"status": 200, "message": "Updated successfully", "data": sub_category}


@router.delete("/delete", response_model=APIResponse[SubCategoryResponse])
def delete_api(
    uu_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    sub_category = soft_delete_sub_category(db, uu_id)
    return {"status": 200, "message": "Deleted successfully", "data": sub_category}
