from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.response import APIResponse
from app.services.user_service import create_user, get_users

router = APIRouter()


@router.post("/create",response_model=APIResponse[UserResponse])
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user)
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

