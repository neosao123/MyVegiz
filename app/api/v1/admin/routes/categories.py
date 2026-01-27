from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from fastapi import Request

from app.api.dependencies import get_db
from app.schemas.category import CategoryCreate, CategoryResponse,CategoryUpdate
from app.schemas.response import APIResponse,PaginatedAPIResponse
from app.services.category_service import create_category, get_categories

from app.services.category_service import update_category
from app.services.category_service import soft_delete_category

from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.category import Category
router = APIRouter()


# Pagination
from fastapi import Query
import math


@router.post("/create", response_model=APIResponse[CategoryResponse])
def add_category(
    category: CategoryCreate = Depends(CategoryCreate.as_form),
    category_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    new_category = create_category(db, category, category_image)

    return {
        "status": 201,
        "message": "Category created successfully",
        "data": new_category
    }



@router.get("/list", response_model=PaginatedAPIResponse[List[CategoryResponse]])
def list_categories(
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
        base_query = db.query(Category).filter(
            Category.is_delete == False
        ).order_by(Category.created_at.desc())

        total_records = base_query.count()

        categories = base_query.offset(offset).limit(limit).all()

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

    except Exception as e:
        return {
            "status": 500,
            "message": "Failed to fetch categories",
            "data": [],
            "pagination": {
                "total": 0,
                "per_page": limit,
                "current_page": page,
                "total_pages": 0
            }
        }





@router.put("/update", response_model=APIResponse[CategoryResponse])
def update_category_api(
    uu_id: str,  # query param
    category: CategoryUpdate = Depends(CategoryUpdate.as_form),
    category_image: UploadFile = File(None),
    db: Session = Depends(get_db),    
    current_user: User = Depends(get_current_user)

):
    updated_category = update_category(
        db,
        uu_id,
        category,
        category_image
    )

    return {
        "status": 200,
        "message": "Category updated successfully",
        "data": updated_category
    }





@router.delete("/delete", response_model=APIResponse[CategoryResponse])
def delete_category_api(
    uu_id: str,   # query parameter
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    deleted_category = soft_delete_category(db, uu_id)

    return {
        "status": 200,
        "message": "Category deleted successfully",
        "data": deleted_category
    }



