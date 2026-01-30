# app/api/v1/routes/main_categories.py
from app.models import main_category
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
import math

from app.api.dependencies import get_db
from app.schemas.main_category import (
    MainCategoryCreate,
    MainCategoryUpdate,
    MainCategoryResponse
)
from app.schemas.response import APIResponse, PaginatedAPIResponse
from app.services.main_category_service import (
    create_main_category,
    list_main_categories,
    update_main_category
)
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/create", response_model=APIResponse[MainCategoryResponse])
def create_api(
    data: MainCategoryCreate = Depends(MainCategoryCreate.as_form),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    category = create_main_category(db, data, image)
    return {"status": 201, "message": "Created successfully", "data": category}


@router.get("/list", response_model=PaginatedAPIResponse[list[MainCategoryResponse]])
def list_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        # -------------------------------
        # Pagination
        # -------------------------------
        offset = (page - 1) * limit

        # -------------------------------
        # Fetch sliders
        # -------------------------------
        total_records, main_categories = list_main_categories(db, offset, limit)

        total_pages = math.ceil(total_records / limit) if limit else 1

        pagination = {
                "total": total_records,
                "per_page": limit,
                "current_page": page,
                "total_pages": total_pages,
            }

        if main_categories:
                return {
                    "status": 200,
                    "message": "main categories fetched successfully",
                    "data": main_categories,
                    "pagination": pagination
                }

        return {
                "status": 300,
                "message": "No main categories found",
                "data": [],
                "pagination": pagination
            }

    except Exception:
            return {
                "status": 500,
                "message": "Failed to fetch sliders",
                "data": [],
            }


@router.put("/update", response_model=APIResponse[MainCategoryResponse])
def update_api(
    uu_id: str,
    data: MainCategoryUpdate = Depends(MainCategoryUpdate.as_form),
    main_category_image: UploadFile = File(None),  # 👈 CHANGE HERE
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    category = update_main_category(db, uu_id, data, main_category_image)
    return {"status": 200, "message": "Updated successfully", "data": category}
