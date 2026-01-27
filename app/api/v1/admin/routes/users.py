from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.response import APIResponse,PaginatedAPIResponse
from app.services.user_service import create_user, get_users
from fastapi import Depends


from app.schemas.user import UserUpdate 
from app.services.user_service import update_user
from app.services.user_service import soft_delete_user


from app.api.dependencies import get_current_user
from app.models.user import User
router = APIRouter()


# Pagination
from fastapi import Query
import math


@router.post("/create",response_model=APIResponse[UserResponse])
def add_user(
    user: UserCreate = Depends(UserCreate.as_form),
    profile_image: UploadFile = File(None), 
    db: Session = Depends(get_db),    
    current_user: User = Depends(get_current_user)
):
    user = create_user(db, user, profile_image)
    return {
        "status": 201,
        "message": "User created successfully",
        "data": user
    }


@router.get("/list",response_model=PaginatedAPIResponse[List[UserResponse]])
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    try:
        # -------------------------------
        # Pagination inputs (Django style)
        # -------------------------------
        offset = (page - 1) * limit

        # -------------------------------
        # Base filters (soft delete aware)
        # -------------------------------
        base_query = db.query(User).filter(
            User.is_delete == False
        ).order_by(User.created_at.desc())

        total_records = base_query.count()

        users = base_query.offset(offset).limit(limit).all()


        # -------------------------------
        # Pagination info
        # -------------------------------
        total_pages = math.ceil(total_records / limit) if limit else 1

        pagination = {
            "total": total_records,
            "per_page": limit,
            "current_page": page,
            "total_pages": total_pages,
        }

        # -------------------------------
        # Response
        # -------------------------------
        if users:
            return {
                "status": 200,
                "message": "Users fetched successfully",
                "data": users,
                "pagination": pagination
            }

        return {
            "status": 300,
            "message": "No users found",
            "data": [],
            "pagination": pagination
        }

    except Exception as e:
        return {
            "status": 500,
            "message": "Failed to fetch users",
            "data": [],
        }





@router.put("/update", response_model=APIResponse[UserResponse])
def update_user_api(
    uu_id: str,  # ✅ STRING UUID
    profile_image: UploadFile = File(None),
    user: UserUpdate = Depends(UserUpdate.as_form),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    updated_user = update_user(db, uu_id, user, profile_image)

    return {
        "status": 200,
        "message": "User updated successfully",
        "data": updated_user
    }



@router.delete("/delete", response_model=APIResponse[UserResponse])
def delete_user_api(
    uu_id: str,  # ✅ STRING UUID
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    deleted_user = soft_delete_user(db, uu_id)

    return {
        "status": 200,
        "message": "User deleted successfully",
        "data": deleted_user
    }
