from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from fastapi import Request,Query
import math
from app.api.dependencies import get_db,get_current_user
from app.schemas.category import CategoryCreate, CategoryResponse,CategoryUpdate,MainCategoryDropdownResponse
from app.schemas.response import APIResponse,PaginatedAPIResponse
from app.services.category_service import create_category,soft_delete_category,update_category,list_categories,get_main_category_dropdown,search_categories
from app.models.user import User
from app.models.category import Category

router = APIRouter()


# -------------------------------
# create category 
# -------------------------------
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


# -------------------------------
# list of all categories
# -------------------------------
@router.get("/list", response_model=PaginatedAPIResponse[List[CategoryResponse]])
def list_categories_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    q: str | None = Query(None, description="Search category"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # -------------------------------
        # Pagination calculation
        # -------------------------------
        offset = (page - 1) * limit

        if q:
            total_records, categories = search_categories(
                db=db,
                search=q,
                offset=offset,
                limit=limit
            )
        else:

            total_records, categories = list_categories(db, offset, limit)

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

    except Exception:
        return {
            "status": 500,
            "message": "Failed to fetch categories",
            "data": [],
        }



# -------------------------------
# update category uu_id wise
# -------------------------------
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






# -------------------------------
# delete category uu_id wise
# -------------------------------
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


# -------------------------------
# dropdown of main category 
# -------------------------------
@router.get(
    "/dropdown",
    response_model=APIResponse[List[MainCategoryDropdownResponse]]
)
def main_category_dropdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    categories = get_main_category_dropdown(db)

    if not categories:
        return {
            "status": 300,
            "message": "No main categories found",
            "data": []
        }

    return {
        "status": 200,
        "message": "Main categories fetched successfully",
        "data": categories
    }
