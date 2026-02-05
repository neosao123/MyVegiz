from fastapi import APIRouter, Depends, UploadFile, File,Form
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_current_user
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse,CategoryDropdownResponse,SubCategoryDropdownResponse,ProductImageResponse
from app.schemas.response import APIResponse,PaginatedAPIResponse
from app.services.product_service import (
    create_product,
    list_products,
    update_product,
    soft_delete_product,
    get_category_dropdown,
    get_sub_category_dropdown_by_category_uu_id,
    search_products
)
from app.models.user import User
from app.models.product import Product
from app.models.product_image import ProductImage
from app.core.exceptions import AppException
from fastapi import Query
import math

router = APIRouter()


# -------------------------------
# create products
# -------------------------------
@router.post("/create", response_model=APIResponse[ProductResponse])
def add_product(
    product: ProductCreate = Depends(ProductCreate.as_form),
    images: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = create_product(db, product, images)
    return {"status": 201, "message": "Product created successfully", "data": data}


# -------------------------------
# list of products
# -------------------------------
@router.get("/list", response_model=PaginatedAPIResponse[List[ProductResponse]])
def list_products_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    q: str | None = Query(None, description="Search keyword"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # -------------------------------
        # Pagination calculation
        # -------------------------------
        offset = (page - 1) * limit

        if q:
            total_records, products = search_products(
                db=db,
                search=q,
                offset=offset,
                limit=limit
            )
        else:
            total_records, products = list_products(db, offset, limit)

        # -------------------------------
        # Fetch sliders
        # -------------------------------
        # total_records, products = list_products(db, offset, limit)

        total_pages = math.ceil(total_records / limit) if limit else 1

        pagination = {
            "total": total_records,
            "per_page": limit,
            "current_page": page,
            "total_pages": total_pages,
        }

        if products:
            return {
                "status": 200,
                "message": "Products fetched successfully",
                "data": products,
                "pagination": pagination
            }

        return {
            "status": 300,
            "message": "No Products found",
            "data": [],
            "pagination": pagination
        }

    except Exception:
            return {
                "status": 500,
                "message": "Failed to fetch Products",
                "data": [],
            }


# -------------------------------
# update products uu_id wise
# -------------------------------
@router.put("/update", response_model=APIResponse[ProductResponse])
def update_product_api(
    uu_id: str,    
    product: ProductUpdate = Depends(ProductUpdate.as_form),
    removed_image_ids: List[int] = Form(default_factory=list),
    images: List[UploadFile] = File(default_factory=list),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = update_product(db, uu_id, product, removed_image_ids=removed_image_ids,
        images=images)
 

    return {"status": 200, "message": "Product updated successfully", "data": data}

# -------------------------------
# delete products uu_id wise
# -------------------------------
@router.delete("/delete", response_model=APIResponse[ProductResponse])
def delete_product_api(
    uu_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = soft_delete_product(db, uu_id)
    return {"status": 200, "message": "Product deleted successfully", "data": data}



# -------------------------------
# dropdown of category 
# -------------------------------
@router.get(
    "/dropdown-category",
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



# -------------------------------
# dropdown of subcategory 
# -------------------------------
@router.get(
    "/dropdown-subcategory",
    response_model=APIResponse[List[SubCategoryDropdownResponse]]
)
def sub_category_dropdown(
    category_uu_id: str = Query(..., description="Category UUID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sub_categories = get_sub_category_dropdown_by_category_uu_id(
        db=db,
        category_uu_id=category_uu_id
    )

    if not sub_categories:
        return {
            "status": 300,
            "message": "No sub categories found",
            "data": []
        }

    return {
        "status": 200,
        "message": "Sub categories fetched successfully",
        "data": sub_categories
    }