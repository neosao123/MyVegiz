from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.uom import UOMCreate, UOMUpdate, UOMResponse
from app.schemas.response import APIResponse,PaginatedAPIResponse
from app.services.uom_service import (
    create_uom,
    list_uoms,
    update_uom,
    soft_delete_uom,
    search_uoms
)
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.uom import UOM
router = APIRouter()


# Pagination
from fastapi import Query
import math

# -------------------------------
# create uoms
# -------------------------------
@router.post("/create", response_model=APIResponse[UOMResponse])
def add_uom(
    uom: UOMCreate = Depends(UOMCreate.as_form),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = create_uom(db, uom)
    return {
        "status": 201,
        "message": "UOM created successfully",
        "data": result
    }


# -------------------------------
# list of uoms
# -------------------------------
@router.get("/list", response_model=PaginatedAPIResponse[List[UOMResponse]])
def list_uoms_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    q: str | None = Query(None, description="Search UOM"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # -------------------------------
        # Pagination calculation
        # -------------------------------
        offset = (page - 1) * limit


        if q:
            total_records, uoms = search_uoms(
                db=db,
                search=q,
                offset=offset,
                limit=limit
            )
        else:
            total_records, uoms = list_uoms(db, offset, limit)

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
        if uoms:
            return {
                "status": 200,
                "message": "UOM list fetched successfully",
                "data": uoms,
                "pagination": pagination
            }

        return {
            "status": 300,
            "message": "No UOMs found",
            "data": [],
            "pagination": pagination
        }

    except Exception:
        return {
            "status": 500,
            "message": "Failed to fetch UOMs",
            "data": [],
        }



# -------------------------------
# update uoms uu_id wise
# -------------------------------
@router.put("/update", response_model=APIResponse[UOMResponse])
def update_uom_api(
    uu_id: str,
    uom: UOMUpdate = Depends(UOMUpdate.as_form),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = update_uom(db, uu_id , uom)
    return {
        "status": 200,
        "message": "UOM updated successfully",
        "data": result
    }



# -------------------------------
# delete uoms uu_id wise
# -------------------------------
@router.delete("/delete", response_model=APIResponse[UOMResponse])
def delete_uom_api(
    uu_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = soft_delete_uom(db, uu_id)
    return {
        "status": 200,
        "message": "UOM deleted successfully",
        "data": result
    }
