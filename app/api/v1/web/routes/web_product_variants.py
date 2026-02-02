from fastapi import APIRouter, Depends, status,Query
from sqlalchemy.orm import Session
from typing import List
import math

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.response import APIResponse
from app.schemas.web_product_variants import ProductVariantResponse

from app.services.web_product_variants_service import list_all_product_variants
from app.schemas.response import APIResponse, PaginatedAPIResponse
from fastapi import HTTPException



router = APIRouter()



@router.get(
    "/list",
    response_model=PaginatedAPIResponse[List[ProductVariantResponse]]
)
def list_all_product_variants_api(
    lat: float = Query(...),
    lng: float = Query(...),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    main_category_slug: str | None = Query(None),
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user),
):
    offset = (page - 1) * limit

    try:
        total_records, variants, error_message = list_all_product_variants(
            db, lat, lng, offset, limit,main_category_slug=main_category_slug
        )

        if error_message:
            return {
                "status": 400,
                "message": error_message,
                "data": [],
                "pagination": {
                    "total": 0,
                    "per_page": limit,
                    "current_page": page,
                    "total_pages": 0,
                }
            }


        total_pages = math.ceil(total_records / limit) if limit else 1

        pagination = {
            "total": total_records,
            "per_page": limit,
            "current_page": page,
            "total_pages": total_pages,
        }

        return {
            "status": 200,
            "message": "Product variants fetched successfully",
            "data": variants,
            "pagination": pagination,
        }
    
    except Exception as e:
        # Return error with status 500 inside, but HTTP 200
        return {
            "status": 500,
            "message": "Failed to fetch product variants",
            "data": [],
            "pagination": {
                "total": 0,
                "per_page": limit,
                "current_page": page,
                "total_pages": 0,
            }
        }
