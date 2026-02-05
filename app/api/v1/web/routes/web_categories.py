from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import math

from app.api.dependencies import get_db
from app.schemas.response import PaginatedAPIResponse
from app.schemas.web_category import CategoryResponse
from app.services.web_category_service import list_web_categories

router = APIRouter()


# -------------------------
# LIST for Category
# -------------------------
@router.get("/list",response_model=PaginatedAPIResponse[list[CategoryResponse]])
def list_categories_web(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    main_category_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    try:
        # -------------------------------
        # Pagination
        # -------------------------------
        offset = (page - 1) * limit

        total_records, categories = list_web_categories(
            db, offset, limit,main_category_id=main_category_id
        )

        total_pages = math.ceil(total_records / limit) if limit else 1

        pagination = {
            "total": total_records,
            "per_page": limit,
            "current_page": page,
            "total_pages": total_pages,
        }

        # -------------------------------
        # Response (LIKE MAIN CATEGORY)
        # -------------------------------
        if categories:
            return {
                "status": 200,
                "message": "Categories fetched successfully",
                "data": categories,
                "pagination": pagination
            }

        return {
            "status": 300,
            "message": "No categories found",
            "data": [],
            "pagination": pagination
        }

    except Exception:
        return {
            "status": 500,
            "message": "Failed to fetch categories",
            "data": []
        }
