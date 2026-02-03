from fastapi import APIRouter, Depends, status,Query
from sqlalchemy.orm import Session
from typing import List
import math

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.response import APIResponse
from app.schemas.product_variant import ProductVariantBulkCreate,ProductVariantResponse,ZoneDropdownResponse,UOMDropdownResponse,ProductDropdownResponse

from app.services.product_variant_service import bulk_create_product_variants,list_all_product_variants,update_product_variant,soft_delete_product_variant,list_uom_dropdown,list_zone_dropdown,list_product_dropdown
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
    try:

        offset = (page - 1) * limit

        # -------------------------------
        # Fetch sliders
        # -------------------------------
        total_records, variants = list_all_product_variants(db, offset, limit)

        total_pages = math.ceil(total_records / limit) if limit else 1

        pagination = {
            "total": total_records,
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

    except Exception:
        return {
            "status": 500,
            "message": "Failed to fetch product variants",
            "data": [],
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






@router.get(
    "/zones",
    response_model=APIResponse[List[ZoneDropdownResponse]]
)
def zone_dropdown_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    zones = list_zone_dropdown(db)

    return {
        "status": 200,
        "message": "Zones fetched successfully",
        "data": [
            {
                "zone_id": z.id,
                "zone_name": z.zone_name
            } for z in zones
        ]
    }



@router.get(
    "/uoms",
    response_model=APIResponse[List[UOMDropdownResponse]]
)
def uom_dropdown_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    uoms = list_uom_dropdown(db)

    return {
        "status": 200,
        "message": "UOMs fetched successfully",
        "data": [
            {
                "uom_id": u.id,
                "uom_name": u.uom_name
            } for u in uoms
        ]
    }



@router.get(
    "/products",
    response_model=APIResponse[List[ProductDropdownResponse]]
)
def product_dropdown_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    products = list_product_dropdown(db)

    return {
        "status": 200,
        "message": "Products fetched successfully",
        "data": [
            {
                "product_id": p.id,
                "product_name": p.product_name
            } for p in products
        ]
    }
