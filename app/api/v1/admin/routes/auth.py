from fastapi import APIRouter, Depends,Header
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user

from app.api.dependencies import get_db
from app.schemas.auth import LoginRequest, LoginResponse, RefreshTokenRequest
from app.schemas.response import APIResponse
from app.services.auth_service import login_user, refresh_access_token
from app.models.token_blacklist import TokenBlacklist

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
def refresh_token(payload: RefreshTokenRequest,db: Session = Depends(get_db)
):
    data = refresh_access_token(payload.refresh_token,db)
    return {
        "status": 200,
        "message": "Token refreshed",
        "data": data
    }





@router.post("/logout", response_model=APIResponse[None])
def logout(
    authorization: str = Header(...),
    refresh_token: str = Header(...),
    db: Session = Depends(get_db)
):
    access_token = authorization.split(" ")[1]

    tokens = [access_token, refresh_token]

    for token in tokens:
        exists = db.query(TokenBlacklist).filter(
            TokenBlacklist.token == token
        ).first()

        if not exists:
            db.add(TokenBlacklist(token=token))

    db.commit()

    return {
        "status": 200,
        "message": "Logged out successfully",
        "data": None
    }