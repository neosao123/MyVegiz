# app/api/v1/restaurant/routes/entity_category.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import math

from app.api.dependencies import get_db

from app.schemas.response import APIResponse, PaginatedAPIResponse

from app.schemas.restaurant_entity_category import (
    EntityCategoryCreate,
    EntityCategoryUpdate,
    EntityCategoryResponse
)
from app.services.restaurant_entity_category_service import (
    create_entity_category,
    list_entity_categories,
    update_entity_category,
    delete_entity_category   
)

router = APIRouter()


@router.post("/create", response_model=APIResponse[EntityCategoryResponse])
def create_entity_category_api(
    data: EntityCategoryCreate = Depends(EntityCategoryCreate.as_form),
    db: Session = Depends(get_db),
):
    entity = create_entity_category(db, data)
    return {
        "status": 201,
        "message": "Entity category created successfully",
        "data": entity
    }



@router.get("/list",response_model=PaginatedAPIResponse[list[EntityCategoryResponse]])
def list_entity_category_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    main_category_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    try:
        offset = (page - 1) * limit

        total_records, entities = list_entity_categories(
            db=db,
            offset=offset,
            limit=limit,
            main_category_id=main_category_id
        )

        total_pages = math.ceil(total_records / limit) if limit else 1

        pagination = {
            "total": total_records,
            "per_page": limit,
            "current_page": page,
            "total_pages": total_pages,
        }

        if entities:
            return {
                "status": 200,
                "message": "Entity categories fetched successfully",
                "data": entities,
                "pagination": pagination
            }

        return {
            "status": 300,
            "message": "No entity categories found",
            "data": [],
            "pagination": pagination
        }

    except Exception:
        return {
            "status": 500,
            "message": "Failed to fetch entity categories",
            "data": [],
        }
    




@router.put("/update",response_model=APIResponse[EntityCategoryResponse])
def update_entity_category_api(
    uu_id: str,
    data: EntityCategoryUpdate = Depends(EntityCategoryUpdate.as_form),
    db: Session = Depends(get_db),
):
    entity = update_entity_category(db, uu_id, data)
    return {
        "status": 200,
        "message": "Entity category updated successfully",
        "data": entity
    }




@router.delete("/delete",response_model=APIResponse[EntityCategoryResponse])
def delete_entity_category_api(
    uu_id: str,
    db: Session = Depends(get_db),
):
    entity = delete_entity_category(db, uu_id)
    return {
        "status": 200,
        "message": "Entity category deleted successfully",
        "data": entity
    }

