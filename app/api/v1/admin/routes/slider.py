from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.schemas.slider import SliderCreate, SliderResponse,SliderUpdate
from app.schemas.response import APIResponse,PaginatedAPIResponse
from app.services.slider_service import create_slider,list_sliders,update_slider,soft_delete_slider,search_sliders
from app.models.user import User
from fastapi import Query
import math


router = APIRouter()

# -------------------------------
# create slider
# -------------------------------
@router.post("/create", response_model=APIResponse[SliderResponse])
def create_slider_api(
    data: SliderCreate = Depends(SliderCreate.as_form),
    mobile_image: UploadFile = File(None),
    tab_image: UploadFile = File(None),
    web_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    slider = create_slider(
        db=db,
        data=data,
        mobile_image=mobile_image,
        tab_image=tab_image,
        web_image=web_image
    )

    return {
        "status": 201,
        "message": "Slider created successfully",
        "data": slider
    }


# -------------------------------
# list of slider
# -------------------------------
@router.get("/list", response_model=PaginatedAPIResponse[list[SliderResponse]])
def list_slider_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    q: str | None = Query(None, description="Search by caption"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        # -------------------------------
        # Pagination
        # -------------------------------
        offset = (page - 1) * limit

        if q:
            total_records, sliders = search_sliders(
                db=db,
                search=q,
                offset=offset,
                limit=limit
            )
        else:
            total_records, sliders = list_sliders(db, offset, limit)

        total_pages = math.ceil(total_records / limit) if limit else 1

        pagination = {
            "total": total_records,
            "per_page": limit,
            "current_page": page,
            "total_pages": total_pages,
        }

        if sliders:
            return {
                "status": 200,
                "message": "Sliders fetched successfully",
                "data": sliders,
                "pagination": pagination
            }

        return {
            "status": 300,
            "message": "No sliders found",
            "data": [],
            "pagination": pagination
        }

    except Exception:
        return {
            "status": 500,
            "message": "Failed to fetch sliders",
            "data": [],
        }


# -------------------------------
# update of slider slider_id wise
# -------------------------------
@router.put("/update", response_model=APIResponse[SliderResponse])
def update_slider_api(
    slider_id: int,
    data: SliderUpdate = Depends(SliderUpdate.as_form),
    mobile_image: UploadFile = File(None),
    tab_image: UploadFile = File(None),
    web_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    slider = update_slider(
        db=db,
        slider_id=slider_id,
        data=data,
        mobile_image=mobile_image,
        tab_image=tab_image,
        web_image=web_image
    )

    return {
        "status": 200,
        "message": "Slider updated successfully",
        "data": slider
    }



# -------------------------------
# delete of slider slider_id wise
# -------------------------------
@router.delete("/delete", response_model=APIResponse[SliderResponse])
def delete_slider_api(
    slider_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    slider = soft_delete_slider(db, slider_id)

    return {
        "status": 200,
        "message": "Slider deleted successfully",
        "data": slider
    }
