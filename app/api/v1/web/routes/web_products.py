from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import math

from app.api.dependencies import get_db
from app.models.product import Product
from app.schemas.web_product import ProductResponse
from app.schemas.response import PaginatedAPIResponse

router = APIRouter()

from app.services.web_product_service import list_web_products


# -------------------------
# LIST for Product
# -------------------------
@router.get(
    "/list",
    response_model=PaginatedAPIResponse[List[ProductResponse]]
)
def list_products_web(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    category_id: Optional[int] = Query(None),
    sub_category_id: Optional[int] = Query(None),
    slug: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    try:
        # -------------------------------
        # Pagination
        # -------------------------------
        offset = (page - 1) * limit

        total_records, products = list_web_products(
            db=db,
            offset=offset,
            limit=limit,
            category_id=category_id,
            sub_category_id=sub_category_id,
            slug=slug,   
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
        if products:
            return {
                "status": 200,
                "message": "Products fetched successfully",
                "data": products,
                "pagination": pagination
            }

        return {
            "status": 300,
            "message": "No products found",
            "data": [],
            "pagination": pagination
        }

    except Exception:
        return {
            "status": 500,
            "message": "Failed to fetch products",
            "data": []
        }
