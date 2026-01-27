from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.uom import UOMCreate, UOMUpdate, UOMResponse
from app.schemas.response import APIResponse,PaginatedAPIResponse
from app.services.uom_service import (
    create_uom,
    get_uoms,
    update_uom,
    soft_delete_uom
)
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.uom import UOM
router = APIRouter()


# Pagination
from fastapi import Query
import math

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



@router.get("/list", response_model=PaginatedAPIResponse[List[UOMResponse]])
def list_uoms(
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
        base_query = db.query(UOM).filter(
            UOM.is_delete == False
        ).order_by(UOM.created_at.desc())

        total_records = base_query.count()

        uoms = base_query.offset(offset).limit(limit).all()

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

    except Exception as e:
        return {
            "status": 500,
            "message": "Failed to fetch UOM list",
            "data": [],
            "pagination": {
                "total": 0,
                "per_page": limit,
                "current_page": page,
                "total_pages": 0
            }
        }




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
