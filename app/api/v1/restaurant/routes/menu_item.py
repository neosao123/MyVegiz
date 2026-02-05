from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import math
from fastapi import UploadFile, File


from app.api.dependencies import get_db
from app.schemas.response import APIResponse, PaginatedAPIResponse
from app.schemas.restaurant_menu_item import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemResponse,
    MenuDropdownResponse,
    MenuCategoryDropdownResponse
)
from app.services.restaurant_menu_item_service import (
    create_menu_item,
    list_menu_items,
    update_menu_item,
    delete_menu_item,
    get_menu_dropdown,
    get_menu_category_dropdown
)

router = APIRouter()


# -------------------------
# CREATE Menu Item
# -------------------------
@router.post("/create", response_model=APIResponse[MenuItemResponse])
def create_menu_item_api(
    data: MenuItemCreate = Depends(MenuItemCreate.as_form),
    item_image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    return {
        "status": 201,
        "message": "Menu item created successfully",
        "data": create_menu_item(db, data, item_image)
    }



# -------------------------
# LIST for Menu Item
# -------------------------
@router.get("/list",response_model=PaginatedAPIResponse[list[MenuItemResponse]])
def list_menu_item_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    menu_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    
    try:
        offset = (page - 1) * limit
        total, items = list_menu_items(db, offset, limit, menu_id)

        total_pages = math.ceil(total / limit) if limit else 1

        pagination = {
                "total": total,
                "per_page": limit,
                "current_page": page,
                "total_pages": total_pages,
            }
        

        if items:
                return {
                    "status": 200,
                    "message": "Menu items fetched successfully",
                    "data": items,
                    "pagination": pagination
                }
        
        return {
                "status": 300,
                "message": "No Menu items found",
                "data": [],
                "pagination": pagination
            }
    
    except Exception:
            return {
                "status": 500,
                "message": "Failed to fetch Menu items",
                "data": [],
            }



# -------------------------
# UPDATE Menu Item
# -------------------------
@router.put("/update", response_model=APIResponse[MenuItemResponse])
def update_menu_item_api(
    uu_id: str,
    data: MenuItemUpdate = Depends(MenuItemUpdate.as_form),
    item_image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    return {
        "status": 200,
        "message": "Menu item updated successfully",
        "data": update_menu_item(db, uu_id, data, item_image)
    }


# -------------------------
# DELETE Menu Item
# -------------------------
@router.delete("/delete", response_model=APIResponse[MenuItemResponse])
def delete_menu_item_api(
    uu_id: str,
    db: Session = Depends(get_db),
):
    item = delete_menu_item(db, uu_id)
    return {
        "status": 200,
        "message": "Menu item deleted successfully",
        "data": item
    }



# -------------------------
# MENU DROPDOWN
# -------------------------
@router.get(
    "/menu",
    response_model=APIResponse[list[MenuDropdownResponse]]
)
def menu_dropdown_api(
    db: Session = Depends(get_db)
):
    data = get_menu_dropdown(db)

    return {
        "status": 200,
        "message": "Menu dropdown fetched successfully",
        "data": data
    }


# -------------------------
# MENU CATEGORY DROPDOWN
# -------------------------
@router.get(
    "/menu_category",
    response_model=APIResponse[list[MenuCategoryDropdownResponse]]
)
def menu_category_dropdown_api(
    menu_id: int = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    data = get_menu_category_dropdown(db, menu_id)

    return {
        "status": 200,
        "message": "Menu category dropdown fetched successfully",
        "data": data
    }