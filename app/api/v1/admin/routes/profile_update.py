from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.schemas.response import APIResponse
from app.schemas.profile_update import UserUpdate
from app.models.user import User
from app.services.profile_service import update_user_profile

router = APIRouter()


@router.put("/profile_update", response_model=APIResponse[dict])
def update_profile_api(
    user_data: UserUpdate = Depends(UserUpdate.as_form),
    profile_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_user = update_user_profile(
        db=db,
        user=current_user,
        user_data=user_data,
        profile_image=profile_image
    )

    return {
        "status": 200,
        "message": "Profile updated successfully",
        "data": {
            "id": updated_user.id,
            "name": updated_user.name,
            "email": updated_user.email,
            "contact": updated_user.contact,
            "profile_image": updated_user.profile_image
        }
    }
