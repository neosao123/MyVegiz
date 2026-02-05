from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import UploadFile
from sqlalchemy.sql import func

from app.models.user import User
from app.schemas.profile_update import UserUpdate
from app.core.security import hash_password
from app.core.exceptions import AppException
import cloudinary.uploader

MAX_IMAGE_SIZE = 1 * 1024 * 1024  # 1MB
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]


# ============================================================
# UPLOAD PROFILE IMAGE TO CLOUDINARY
# ============================================================
def upload_profile_image(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise AppException(status=400, message="Only JPG and PNG images allowed")

    contents = file.file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise AppException(status=400, message="Profile image must be under 1MB")

    result = cloudinary.uploader.upload(
        contents,
        folder="myvegiz/users",
        resource_type="image"
    )
    return result["secure_url"]

# ============================================================
# UPDATE USER PROFILE
# ============================================================
def update_user_profile(
    db: Session,
    user: User,
    user_data: UserUpdate,
    profile_image: UploadFile = None
):
    # ---------- NAME ----------
    if user_data.name is not None:
        user.name = user_data.name

    # ---------- EMAIL ----------
    if user_data.email is not None:
        email_exists = db.query(User).filter(
            User.email == user_data.email,
            User.id != user.id,
            User.is_delete == False
        ).first()
        if email_exists:
            raise AppException(status=400, message="Email already exists")
        user.email = user_data.email

    # ---------- CONTACT ----------
    if user_data.contact is not None:
        user.contact = user_data.contact

    # ---------- PASSWORD ----------
    if user_data.password is not None:
        user.password = hash_password(user_data.password)

    # ---------- PROFILE IMAGE ----------
    if profile_image:
        user.profile_image = upload_profile_image(profile_image)

    user.is_update = True
    user.updated_at = func.now()

    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error while updating profile")
