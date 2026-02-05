from sqlalchemy.orm import Session
from fastapi import UploadFile
import cloudinary.uploader

from app.models.slider import Slider
from app.core.exceptions import AppException

from sqlalchemy.sql import func


# =====================================================
# LIST SLIDERS (WEB)
# Fetch active sliders for banners
# Soft-delete & active aware
# =====================================================
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


