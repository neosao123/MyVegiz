from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import math

from app.api.dependencies import get_db
from app.schemas.web_slider import SliderResponse
from app.schemas.response import PaginatedAPIResponse
from app.services.web_slider_service import list_sliders  

router = APIRouter()


# -------------------------
# LIST for Slider
# -------------------------
@router.get("/list", response_model=PaginatedAPIResponse[list[SliderResponse]])
def list_web_sliders(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    try:
        offset = (page - 1) * limit

        total_records, sliders = list_sliders(db, offset, limit)

        total_pages = math.ceil(total_records / limit) if limit else 1

        pagination = {
            "total": total_records,
            "per_page": limit,
            "current_page": page,
            "total_pages": total_pages,
        }

        if sliders:
            return {
                "status": 200,
                "message": "Sliders fetched successfully",
                "data": sliders,
                "pagination": pagination
            }

        return {
            "status": 300,
            "message": "No sliders found",
            "data": [],
            "pagination": pagination
        }

    except Exception:
        return {
            "status": 500,
            "message": "Failed to fetch sliders",
            "data": [],
        }
