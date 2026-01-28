from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.schemas.slider import SliderCreate, SliderResponse
from app.schemas.response import APIResponse
from app.services.slider_service import create_slider
from app.models.user import User

router = APIRouter()


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
