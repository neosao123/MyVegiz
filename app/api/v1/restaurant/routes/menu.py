from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import math

from app.api.dependencies import get_db
from app.schemas.response import APIResponse, PaginatedAPIResponse
from app.schemas.restaurant_menu import (
    MenuCreate,
    MenuUpdate,
    MenuResponse
)
from app.services.restaurant_menu_service import (
    create_menu,
    list_menus,
    update_menu,
    delete_menu
)

router = APIRouter()


# -------------------------
# CREATE Menu
# -------------------------
@router.post("/create", response_model=APIResponse[MenuResponse])
def create_menu_api(
    data: MenuCreate = Depends(MenuCreate.as_form),
    db: Session = Depends(get_db),
):
    menu = create_menu(db, data)
    return {
        "status": 201,
        "message": "Menu created successfully",
        "data": menu
    }



# -------------------------
# LIST for Menu
# -------------------------
@router.get("/list",response_model=PaginatedAPIResponse[list[MenuResponse]])
def list_menu_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    
    try:
        offset = (page - 1) * limit
        total_records, menus = list_menus(db, offset, limit)

        total_pages = math.ceil(total_records / limit) if limit else 1


        pagination = {
                "total": total_records,
                "per_page": limit,
                "current_page": page,
                "total_pages": total_pages,
            }
        
        if menus:
                return {
                    "status": 200,
                    "message": "Menus fetched successfully",
                    "data": menus,
                    "pagination": pagination
                }
        
        return {
                "status": 300,
                "message": "No Menus found",
                "data": [],
                "pagination": pagination
            }

    except Exception:
            return {
                "status": 500,
                "message": "Failed to fetch Menus",
                "data": [],
            }



# -------------------------
# UPDATE Menu
# -------------------------
@router.put("/update", response_model=APIResponse[MenuResponse])
def update_menu_api(
    uu_id: str,
    data: MenuUpdate = Depends(MenuUpdate.as_form),
    db: Session = Depends(get_db),
):
    menu = update_menu(db, uu_id, data)
    return {
        "status": 200,
        "message": "Menu updated successfully",
        "data": menu
    }



# -------------------------
# DELETE Menu
# -------------------------
@router.delete("/delete", response_model=APIResponse[MenuResponse])
def delete_menu_api(
    uu_id: str,
    db: Session = Depends(get_db),
):
    menu = delete_menu(db, uu_id)
    return {
        "status": 200,
        "message": "Menu deleted successfully",
        "data": menu
    }
