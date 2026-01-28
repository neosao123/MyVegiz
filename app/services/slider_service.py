from sqlalchemy.orm import Session
from fastapi import UploadFile
import cloudinary.uploader

from app.models.slider import Slider
from app.schemas.slider import SliderCreate,SliderUpdate
from app.core.exceptions import AppException

from sqlalchemy.sql import func

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



def list_sliders(db: Session, offset: int, limit: int):
    # -------------------------------
    # Base filters (soft delete aware)
    # -------------------------------
    base_query = db.query(Slider).filter(
        Slider.is_delete == False,
        Slider.is_active == True
    ).order_by(Slider.created_at.desc())

    total_records = base_query.count()

    sliders = base_query.offset(offset).limit(limit).all()

    return total_records, sliders




def update_slider(
    db: Session,
    slider_id: int,
    data: SliderUpdate,
    mobile_image: UploadFile = None,
    tab_image: UploadFile = None,
    web_image: UploadFile = None
):
    slider = db.query(Slider).filter(
        Slider.id == slider_id,
        Slider.is_delete == False
    ).first()

    if not slider:
        raise AppException(404, "Slider not found")

    # UPDATE TEXT FIELDS
    if data.caption is not None:
        slider.caption = data.caption

    if data.is_active is not None:
        slider.is_active = data.is_active

    # UPDATE IMAGES (OPTIONAL)
    if mobile_image and mobile_image.filename:
        slider.mobile_image = upload_slider_image(mobile_image, "mobile")

    if tab_image and tab_image.filename:
        slider.tab_image = upload_slider_image(tab_image, "tab")

    if web_image and web_image.filename:
        slider.web_image = upload_slider_image(web_image, "web")

    slider.is_update = True
    slider.updated_at = func.now()

    db.commit()
    db.refresh(slider)

    return slider





def soft_delete_slider(db: Session, slider_id: int):
    slider = db.query(Slider).filter(
        Slider.id == slider_id,
        Slider.is_delete == False
    ).first()

    if not slider:
        raise AppException(404, "Slider not found")

    slider.is_delete = True
    slider.is_active = False
    slider.deleted_at = func.now()

    db.commit()
    db.refresh(slider)

    return slider
