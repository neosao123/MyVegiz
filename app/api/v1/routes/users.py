from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.response import APIResponse
from app.services.user_service import create_user, get_users
from fastapi import Depends


from app.schemas.user import UserUpdate 
from app.services.user_service import update_user

router = APIRouter()


@router.post("/create",response_model=APIResponse[UserResponse])
def add_user(user: UserCreate = Depends(UserCreate.as_form),
             profile_image: UploadFile = File(None), 
             db: Session = Depends(get_db)
):
    user = create_user(db, user, profile_image)
    return {
        "status": 201,
        "message": "User created successfully",
        "data": user
    }


@router.get("/list",response_model=APIResponse[List[UserResponse]])
def list_users(db: Session = Depends(get_db)):
    users = get_users(db)

    if not users:
        return {
            "status": 200,
            "message": "No users found",
            "data": []
        }

    return {
        "status": 200,
        "message": "Users fetched successfully",
        "data": users
    }



@router.put("/update/{user_id}", response_model=APIResponse[UserResponse])
def update_user_api(
    user_id: int,
    profile_image: UploadFile = File(None),   # ✅ FIRST
    user: UserUpdate = Depends(UserUpdate.as_form),  # ✅ AFTER
    db: Session = Depends(get_db)
):
    updated_user = update_user(db, user_id, user, profile_image)

    return {
        "status": 200,
        "message": "User updated successfully",
        "data": updated_user
    }
