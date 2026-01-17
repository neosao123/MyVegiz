from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.auth import LoginRequest, LoginResponse, RefreshTokenRequest
from app.schemas.response import APIResponse
from app.services.auth_service import login_user, refresh_access_token

router = APIRouter()



@router.post("/login", response_model=APIResponse[LoginResponse])
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    data = login_user(db, payload.email, payload.password)
    return {
        "status": 200,
        "message": "Login successful",
        "data": data
    }


@router.post("/refresh", response_model=APIResponse[dict])
def refresh_token(payload: RefreshTokenRequest):
    data = refresh_access_token(payload.refresh_token)
    return {
        "status": 200,
        "message": "Token refreshed",
        "data": data
    }



@router.post("/logout", response_model=APIResponse[None])
def logout():
    # Stateless logout (frontend deletes tokens)
    return {
        "status": 200,
        "message": "Logged out successfully",
        "data": None
    }