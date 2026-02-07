from fastapi import APIRouter, Depends, status, UploadFile, File,Query
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db,get_current_user
from app.schemas.user import UserCreate, UserResponse,UserUpdate
from app.schemas.response import APIResponse,PaginatedAPIResponse
from app.services.user_service import create_user, get_users,update_user,soft_delete_user,search_users
from app.models.user import User
import math

router = APIRouter()

# -------------------------------
# create users for admin
# -------------------------------
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

# -------------------------------
# list of admin users  
# -------------------------------
@router.get("/list",response_model=PaginatedAPIResponse[List[UserResponse]])
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    q: str | None = Query(None, description="Search keyword"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    try:
        # -------------------------------
        # Pagination inputs (Django style)
        # -------------------------------
        offset = (page - 1) * limit


        if q:
            total_records, users = search_users(
                db=db,
                search=q,
                offset=offset,
                limit=limit
            )
        else:
            total_records, users = get_users(db, offset, limit)

 

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

    except Exception:
        return {
            "status": 500,
            "message": "Failed to fetch users",
            "data": [],
        }





# -------------------------------
# update of admin users uu_id wise  
# -------------------------------
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



# -------------------------------
# delete of admin users uu_id wise  
# -------------------------------
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
