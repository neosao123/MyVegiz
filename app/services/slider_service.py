from sqlalchemy.orm import Session
from fastapi import UploadFile
import cloudinary.uploader

from app.models.slider import Slider
from app.schemas.slider import SliderCreate
from app.core.exceptions import AppException


MAX_IMAGE_SIZE = 1 * 1024 * 1024  # 1MB
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]


def upload_slider_image(file: UploadFile, folder: str) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise AppException(400, "Only JPG and PNG images allowed")

    contents = file.file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise AppException(400, "Image must be less than 1MB")

    result = cloudinary.uploader.upload(
        contents,
        folder=f"myvegiz/sliders/{folder}",
        resource_type="image"
    )
    return result["secure_url"]


def create_slider(
    db: Session,
    data: SliderCreate,
    mobile_image: UploadFile = None,
    tab_image: UploadFile = None,
    web_image: UploadFile = None
):
    # REQUIRED IMAGE VALIDATION 
    if not mobile_image or not mobile_image.filename:
        raise AppException(400, "Mobile image is required")

    if not tab_image or not tab_image.filename:
        raise AppException(400, "Tab image is required")

    if not web_image or not web_image.filename:
        raise AppException(400, "Web image is required")

    slider = Slider(
        caption=data.caption,
        is_active=data.is_active
    )

    slider.mobile_image = upload_slider_image(mobile_image, "mobile")
    slider.tab_image = upload_slider_image(tab_image, "tab")
    slider.web_image = upload_slider_image(web_image, "web")

    db.add(slider)
    db.commit()
    db.refresh(slider)

    return slider
