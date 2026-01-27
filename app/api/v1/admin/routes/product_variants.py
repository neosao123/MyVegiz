from fastapi import APIRouter, Depends, status,Query
from sqlalchemy.orm import Session
from typing import List
import math

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.response import APIResponse
from app.schemas.product_variant import ProductVariantBulkCreate,ProductVariantResponse

from app.services.product_variant_service import bulk_create_product_variants,list_all_product_variants,update_product_variant,soft_delete_product_variant
from app.schemas.response import APIResponse, PaginatedAPIResponse
from app.schemas.response import APIResponse

router = APIRouter()


@router.post(
    "/bulk-create",
    response_model=APIResponse[List[ProductVariantResponse]],
    status_code=status.HTTP_201_CREATED
)
def bulk_create_variants_api(
    payload: ProductVariantBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    variants = bulk_create_product_variants(db, payload)

    return {
        "status": 201,
        "message": "Product variants created successfully",
        "data": variants
    }


@router.get(
    "/list",
    response_model=PaginatedAPIResponse[List[ProductVariantResponse]]
)
def list_all_product_variants_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    offset = (page - 1) * limit

    variants, total = list_all_product_variants(
        db=db,
        offset=offset,
        limit=limit
    )

    total_pages = math.ceil(total / limit) if limit else 1

    pagination = {
        "total": total,
        "per_page": limit,
        "current_page": page,
        "total_pages": total_pages,
    }

    if variants:
        return {
            "status": 200,
            "message": "Product variants fetched successfully",
            "data": variants,
            "pagination": pagination,
        }

    return {
        "status": 300,
        "message": "No product variants found",
        "data": [],
        "pagination": pagination,
    }


@router.put(
    "/update",
    response_model=APIResponse[ProductVariantResponse]
)
def update_variant_api(
    uu_id: str,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    variant = update_product_variant(db, uu_id, payload)

    return {
        "status": 200,
        "message": "Product variant updated successfully",
        "data": variant
    }




@router.delete(
    "/delete",
    response_model=APIResponse[ProductVariantResponse]
)
def delete_variant_api(
    uu_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    variant = soft_delete_product_variant(db, uu_id)

    return {
        "status": 200,
        "message": "Product variant deleted successfully",
        "data": variant
    }
