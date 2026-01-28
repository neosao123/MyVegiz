from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.web_auth import WebRegisterRequest
from app.services.web_auth_service import register_and_login_customer

router = APIRouter()



@router.post("/register")
def register(payload: WebRegisterRequest, db: Session = Depends(get_db)):
    data = register_and_login_customer(db, payload)
    return {
        "status": 200,
        "message": "Login successful",
        "data": data
    }
