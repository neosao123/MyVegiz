from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.schemas.system_setting import SystemSettingForm
from app.services.system_setting_service import save_system_settings,list_system_settings
from app.schemas.response import APIResponse
from app.models.user import User
from app.schemas.system_setting import SystemSettingResponse
from typing import List


router = APIRouter(tags=["System Settings"])


# -------------------------------------------------
# SAVE / UPDATE SYSTEM SETTINGS
# -------------------------------------------------
# - Accepts form-data from frontend (single form)
# - First call creates records
# - Subsequent calls update existing records
# - Returns the saved settings in frontend-friendly format
# -------------------------------------------------
@router.post("/save", response_model=APIResponse[List[SystemSettingResponse]])
def save_settings(
    data: SystemSettingForm = Depends(SystemSettingForm.as_form),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    settings = save_system_settings(db, data)

    return {
        "status": 200,
        "message": "System settings saved successfully",
        "data": settings
    }



# -------------------------------------------------
# LIST SYSTEM SETTINGS
# -------------------------------------------------
# - Used to prefill the settings form in frontend
# - Returns parsed values (JSON decoded)
# - Only active & non-deleted settings are returned
# -------------------------------------------------
@router.get("/list",response_model=APIResponse[List[SystemSettingResponse]])
def list_settings(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    settings = list_system_settings(db)

    return {
        "status": 200,
        "message": "System settings fetched successfully",
        "data": settings
    }

