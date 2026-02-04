from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import math
from typing import List

from app.api.dependencies import get_db
from app.models import menu_category
from app.schemas.response import APIResponse, PaginatedAPIResponse
from app.schemas.restaurant_menu_category import (
    MenuCategoryCreate,
    MenuCategoryUpdate,
    MenuCategoryResponse,
    MenuDropdownResponse
)
from app.services.restaurant_menu_category_service import (
    create_menu_category,
    list_menu_categories,
    update_menu_category,
    delete_menu_category,
    list_menu_dropdown
)

router = APIRouter()


@router.post("/create", response_model=APIResponse[MenuCategoryResponse])
def create_menu_category_api(
    data: MenuCategoryCreate = Depends(MenuCategoryCreate.as_form),
    db: Session = Depends(get_db),
):
    entity = create_menu_category(db, data)
    return {
        "status": 201,
        "message": "Menu category created successfully",
        "data": entity
    }


@router.get("/list", response_model=PaginatedAPIResponse[list[MenuCategoryResponse]])
def list_menu_category_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    menu_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    try:
        offset = (page - 1) * limit

        total_records, menu_categories = list_menu_categories(
                db=db,
                offset=offset,
                limit=limit,
                menu_id=menu_id
            )
        
        total_pages = math.ceil(total_records / limit) if limit else 1

        pagination = {
            "total": total_records,
            "per_page": limit,
            "current_page": page,
            "total_pages": math.ceil(total_pages / limit) if limit else 1
        }


        if menu_categories:
            return {
                "status": 200,
                "message": "Menu categories fetched successfully",
                "data": menu_categories,
                "pagination": pagination
            }

        return {
            "status": 300,
            "message": "No Menu categories found",
            "data": [],
            "pagination": pagination
                }

    except Exception:
                return {
                    "status": 500,
                    "message": "Failed to fetch Menu categories",
                    "data": [],
                }


@router.put("/update", response_model=APIResponse[MenuCategoryResponse])
def update_menu_category_api(
    uu_id: str,
    data: MenuCategoryUpdate = Depends(MenuCategoryUpdate.as_form),
    db: Session = Depends(get_db),
):
    entity = update_menu_category(db, uu_id, data)
    return {
        "status": 200,
        "message": "Menu category updated successfully",
        "data": entity
    }


@router.delete("/delete", response_model=APIResponse[MenuCategoryResponse])
def delete_menu_category_api(
    uu_id: str,
    db: Session = Depends(get_db),
):
    entity = delete_menu_category(db, uu_id)
    return {
        "status": 200,
        "message": "Menu category deleted successfully",
        "data": entity
    }


@router.get(
    "/menus",
    response_model=APIResponse[List[MenuDropdownResponse]]
)
def menu_dropdown_api(
    db: Session = Depends(get_db),
):
    menus = list_menu_dropdown(db)

    return {
        "status": 200,
        "message": "Menus fetched successfully",
        "data": [
            {
                "menu_id": m.id,
                "menu_name": m.menu
            } for m in menus
        ]
    }