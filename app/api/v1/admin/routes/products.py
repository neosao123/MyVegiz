

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_current_user
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.schemas.response import APIResponse
from app.api.dependencies import get_db
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)
from app.schemas.response import APIResponse,PaginatedAPIResponse
from app.services.product_service import (
    create_product,
    get_products,
    update_product,
    soft_delete_product
)
from app.models.user import User
from app.models.product import Product

router = APIRouter()

# Pagination
from fastapi import Query
import math


@router.post("/create", response_model=APIResponse[ProductResponse])
def add_product(
    product: ProductCreate = Depends(ProductCreate.as_form),
    images: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = create_product(db, product, images)
    return {"status": 201, "message": "Product created successfully", "data": data}



@router.get("/list", response_model=PaginatedAPIResponse[List[ProductResponse]])
def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # -------------------------------
        # Pagination calculation
        # -------------------------------
        offset = (page - 1) * limit

        # -------------------------------
        # Base query (soft delete aware)
        # -------------------------------
        base_query = db.query(Product).filter(
            Product.is_delete == False
        ).order_by(Product.created_at.desc())

        total_records = base_query.count()

        products = base_query.offset(offset).limit(limit).all()

        # -------------------------------
        # Pagination metadata
        # -------------------------------
        total_pages = math.ceil(total_records / limit) if limit else 1

        pagination = {
            "total": total_records,
            "per_page": limit,
            "current_page": page,
            "total_pages": total_pages,
        }

        # -------------------------------
        # Response
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

    except Exception as e:
        return {
            "status": 500,
            "message": "Failed to fetch products",
            "data": [],
            "pagination": {
                "total": 0,
                "per_page": limit,
                "current_page": page,
                "total_pages": 0
            }
        }



@router.put("/update", response_model=APIResponse[ProductResponse])
def update_product_api(
    uu_id: str,
    product: ProductUpdate = Depends(ProductUpdate.as_form),
    images: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = update_product(db, uu_id, product, images)
    return {"status": 200, "message": "Product updated successfully", "data": data}


@router.delete("/delete", response_model=APIResponse[ProductResponse])
def delete_product_api(
    uu_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = soft_delete_product(db, uu_id)
    return {"status": 200, "message": "Product deleted successfully", "data": data}
