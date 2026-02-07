from app.models import sub_category
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
import math
from typing import List

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.sub_category import (
    SubCategoryCreate,
    SubCategoryUpdate,
    SubCategoryResponse,
    CategoryDropdownResponse
)
from app.schemas.response import APIResponse, PaginatedAPIResponse
from app.services.sub_category_service import (
    create_sub_category,
    list_sub_categories,
    update_sub_category,
    soft_delete_sub_category,
    get_category_dropdown,
    search_sub_categories
)

router = APIRouter()


# -------------------------------
# create  SubCategoryCreate
# -------------------------------
@router.post("/create", response_model=APIResponse[SubCategoryResponse])
def create_api(
    data: SubCategoryCreate = Depends(SubCategoryCreate.as_form),
    sub_category_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    sub_category = create_sub_category(db, data, sub_category_image)
    return {"status": 201, "message": "Created successfully", "data": sub_category}

# -------------------------------
# list of SubCategoryCreate
# -------------------------------
@router.get("/list", response_model=PaginatedAPIResponse[List[SubCategoryResponse]])
def list_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    q: str | None = Query(None, description="Search sub category"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    try:

        # -------------------------------
        # Pagination inputs (Django style)
        # -------------------------------
        offset = (page - 1) * limit

        if q:
            total_records, sub_categories = search_sub_categories(
                db=db,
                search=q,
                offset=offset,
                limit=limit
            )
        else:
            total_records, sub_categories = list_sub_categories(db, offset, limit)

        total_pages = math.ceil(total_records / limit) if limit else 1

        pagination = {
            "total": total_records,
            "per_page": limit,
            "current_page": page,
            "total_pages": total_pages,
        }

        if sub_categories:
            return {
                "status": 200,
                "message": "sub categories fetched successfully",
                "data": sub_categories,
                "pagination": pagination
            }

        return {
            "status": 300,
            "message": "No sub categories found",
            "data": [],
            "pagination": pagination
        }

    except Exception:
        return {
            "status": 500,
            "message": "Failed to fetch sub categories",
            "data": [],
        }


# -------------------------------
# update of SubCategoryCreate uu_id wise
# -------------------------------
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


# -------------------------------
# delete of SubCategoryCreate uu_id wise
# -------------------------------
@router.delete("/delete", response_model=APIResponse[SubCategoryResponse])
def delete_api(
    uu_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    sub_category = soft_delete_sub_category(db, uu_id)
    return {"status": 200, "message": "Deleted successfully", "data": sub_category}



# -------------------------------
# dropdown of category_dropdown
# -------------------------------
@router.get(
    "/dropdown",
    response_model=APIResponse[List[CategoryDropdownResponse]]
)
def category_dropdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    categories = get_category_dropdown(db)

    if not categories:
        return {
            "status": 300,
            "message": "No  categories found",
            "data": []
        }

    return {
        "status": 200,
        "message": "categories fetched successfully",
        "data": categories
    }
