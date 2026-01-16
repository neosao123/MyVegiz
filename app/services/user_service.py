from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.exceptions import AppException

# Business Logic
# Keep logic OUT of routes


def create_user(db: Session, user: UserCreate):

     # Check if email already exists
    if db.query(User).filter(User.email == user.email).first():
        raise AppException(status=400, message="Email already exists")
    
    db_user = User(
        name=user.name,
        email=user.email,
        contact=user.contact,
        password=user.password,  # hash later
        profile_image=user.profile_image,
        is_admin=user.is_admin
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
