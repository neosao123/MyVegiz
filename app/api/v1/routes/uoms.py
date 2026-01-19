from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.uom import UOMCreate, UOMUpdate, UOMResponse
from app.schemas.response import APIResponse
from app.services.uom_service import (
    create_uom,
    get_uoms,
    update_uom,
    soft_delete_uom
)

router = APIRouter()


@router.post("/create", response_model=APIResponse[UOMResponse])
def add_uom(
    uom: UOMCreate = Depends(UOMCreate.as_form),
    db: Session = Depends(get_db)
):
    result = create_uom(db, uom)
    return {
        "status": 201,
        "message": "UOM created successfully",
        "data": result
    }


@router.get("/list", response_model=APIResponse[List[UOMResponse]])
def list_uoms(request: Request, db: Session = Depends(get_db)):
    if request.query_params:
        return {
            "status": 400,
            "message": "Query parameters are not allowed",
            "data": []
        }

    uoms = get_uoms(db)
    return {
        "status": 200,
        "message": "UOM list fetched successfully",
        "data": uoms
    }


@router.put("/update", response_model=APIResponse[UOMResponse])
def update_uom_api(
    uom_id: int,
    uom: UOMUpdate = Depends(UOMUpdate.as_form),
    db: Session = Depends(get_db)
):
    result = update_uom(db, uom_id, uom)
    return {
        "status": 200,
        "message": "UOM updated successfully",
        "data": result
    }


@router.delete("/delete", response_model=APIResponse[UOMResponse])
def delete_uom_api(
    uom_id: int,
    db: Session = Depends(get_db)
):
    result = soft_delete_uom(db, uom_id)
    return {
        "status": 200,
        "message": "UOM deleted successfully",
        "data": result
    }
