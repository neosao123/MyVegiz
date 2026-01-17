from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.exceptions import AppException
from app.core.security import hash_password
from app.schemas.user import UserUpdate
from fastapi import UploadFile


# Business Logic
# Keep logic OUT of routes


import cloudinary.uploader
from fastapi import UploadFile


MAX_IMAGE_SIZE = 1 * 1024 * 1024  # 1MB
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]

def upload_profile_image(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise AppException(status=400, message="Only JPG and PNG images are allowed")

    contents = file.file.read()

    if len(contents) > MAX_IMAGE_SIZE:
        raise AppException(status=400, message="Profile image must be less than 1 MB")

    result = cloudinary.uploader.upload(
        contents,
        folder="myvegiz/users",
        resource_type="image"
    )

    return result["secure_url"]



def create_user(db: Session, user: UserCreate, profile_image: UploadFile = None):


    profile_image_url = None

    if profile_image:
        profile_image_url = upload_profile_image(profile_image)

    #  # Check if email already exists
    # if db.query(User).filter(User.email == user.email).first():
    #     raise AppException(status=400, message="Email already exists")

    # Check EMAIL uniqueness (only active users)
    email_exists = db.query(User).filter(
        User.email == user.email,
        User.is_delete == False,
        User.is_active == True
    ).first()

    if email_exists:
        raise AppException(
            status=400,
            message="Email already exists"
        )

    # Check CONTACT uniqueness (only active users)
    if user.contact:
        contact_exists = db.query(User).filter(
            User.contact == user.contact,
            User.is_delete == False,
            User.is_active == True
        ).first()

        if contact_exists:
            raise AppException(
                status=400,
                message="Contact number already exists"
            )
    
    db_user = User(
        name=user.name,
        email=user.email,
        contact=user.contact,
        password=hash_password(user.password),  # hash later
        profile_image=profile_image_url,
        is_admin=user.is_admin,
        is_active=True
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except IntegrityError as e:
        db.rollback()

        error_msg = str(e.orig)

        # Detect specific DB constraint
        if "users_email" in error_msg or "email" in error_msg:
            raise AppException(status=400, message="Email already exists")

        # Unknown DB error
        raise AppException(
            status=500,
            message="Database error while creating user"
        )


def get_users(db: Session):
    return db.query(User).filter(User.is_delete == False).all()



def update_user(
    db: Session,
    user_id: int,
    user_data: UserUpdate,
    profile_image: UploadFile = None
):
    db_user = db.query(User).filter(
        User.id == user_id,
        User.is_delete == False
    ).first()

    if not db_user:
        raise AppException(status=404, message="User not found")

    # ---------- NAME ----------
    if user_data.name is not None:
        db_user.name = user_data.name

    # ---------- EMAIL ----------
    if user_data.email is not None:
        email_exists = db.query(User).filter(
            User.email == user_data.email,
            User.is_delete == False,
            User.is_active == True,
            User.id != user_id
        ).first()

        if email_exists:
            raise AppException(status=400, message="Email already exists")

        db_user.email = user_data.email

    # ---------- CONTACT ----------
    if user_data.contact is not None:
        contact_exists = db.query(User).filter(
            User.contact == user_data.contact,
            User.is_delete == False,
            User.is_active == True,
            User.id != user_id
        ).first()

        if contact_exists:
            raise AppException(status=400, message="Contact number already exists")

        db_user.contact = user_data.contact

    # ---------- PASSWORD ----------
    if user_data.password is not None:
        db_user.password = hash_password(user_data.password)

    # ---------- PROFILE IMAGE ----------
    if profile_image:
        db_user.profile_image = upload_profile_image(profile_image)

    db_user.is_update = True

    try:
        db.commit()
        db.refresh(db_user)
        return db_user

    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error while updating user")
