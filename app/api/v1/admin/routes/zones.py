from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.zone import ZoneCreate, ZoneUpdate, ZoneResponse
from app.services.zone_service import (
    create_zone,
    list_zones,
    update_zone,
    delete_zone,
    list_all_deliverable_points
)
from app.api.dependencies import get_current_user
from app.models.user import User
router = APIRouter()
from app.schemas.response import APIResponse
from app.schemas.zone import ZoneResponse,ZonePointResponse
from app.services.zone_service import get_zones_by_lat_lng
from app.schemas.response import PaginatedAPIResponse
import math
from typing import List


@router.post("/create", response_model=APIResponse[ZoneResponse])
def create(
    data: ZoneCreate = Depends(ZoneCreate.as_form),
    db: Session = Depends(get_db),    
    current_user: User = Depends(get_current_user)
):
    zone = create_zone(db, data)
    return {
        "status": 201,
        "message": "Zone created successfully",
        "data": zone
    }



@router.get("/list", response_model=PaginatedAPIResponse[list[ZoneResponse]])
def list_zones_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        # -------------------------------
        # Pagination
        # -------------------------------
        offset = (page - 1) * limit

        # -------------------------------
        # Fetch sliders
        # -------------------------------
        total_records, zones = list_zones(db, offset, limit)

        total_pages = math.ceil(total_records / limit) if limit else 1

        pagination = {
            "total": total_records,
            "per_page": limit,
            "current_page": page,
            "total_pages": total_pages,
        }

        if zones:
            return {
                "status": 200,
                "message": "zones fetched successfully",
                "data": zones,
                "pagination": pagination
            }

        return {
            "status": 300,
            "message": "No zones found",
            "data": [],
            "pagination": pagination
        }

    except Exception:
        return {
            "status": 500,
            "message": "Failed to fetch zones",
            "data": [],
        }




@router.put("/update", response_model=APIResponse[ZoneResponse])
def update(
    zone_id: int = Query(..., description="Zone ID"),
    zone_data: ZoneUpdate = Depends(ZoneUpdate.as_form),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    zone = update_zone(db, zone_id, zone_data)

    return {
        "status": 200,
        "message": "Zone updated successfully",
        "data": zone
    }


@router.delete("/delete", response_model=APIResponse[ZoneResponse])
def delete_zone_api(
    zone_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    zone = delete_zone(db, zone_id)

    return {
        "status": 200,
        "message": "Zone deleted successfully",
        "data": zone
    }


@router.get("/list/latitude", response_model=APIResponse[list[ZoneResponse]])
def list_zones_by_lat_lng(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    zones = get_zones_by_lat_lng(db, lat, lng)

    return {
        "status": 200,
        "message": "Zones fetched successfully",
        "data": zones
    }





@router.get(
    "/points",
    response_model=APIResponse[List[ZonePointResponse]]
)
def list_all_zone_points_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    points = list_all_deliverable_points(db)

    return {
        "status": 200,
        "message": "All deliverable zone points fetched successfully",
        "data": points
    }