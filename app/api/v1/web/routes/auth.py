from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.web_auth import WebRegisterRequest
from app.services.web_auth_service import register_customer_send_otp,verify_otp_and_login
from app.schemas.web_auth import (
    MobileSignInRequest,
    MobileOTPVerifyRequest,
    OTPResponse
)
router = APIRouter()



@router.post("/register")
def register(payload: WebRegisterRequest, db: Session = Depends(get_db)):
    data = register_customer_send_otp(db, payload)
    return {
        "status": 200,
        "message": data["message"],
        "data": {"mobile": data["mobile"]}
    }


@router.post("/register/verify-otp")
def verify_otp(payload: MobileOTPVerifyRequest, db: Session = Depends(get_db)):
    data = verify_otp_and_login(db, payload.mobile, payload.otp)
    return {
        "status": 200,
        "message": "Login successful",
        "data": data
    }



from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.web_auth import (
    MobileSignInRequest,
    MobileOTPVerifyRequest,
    OTPResponse
)
from app.services.web_auth_service import send_otp, verify_otp
from app.schemas.response import APIResponse


#sign In
@router.post("/send-otp", response_model=APIResponse[dict])
def request_otp(payload: MobileSignInRequest, db: Session = Depends(get_db)):
    otp_entry = send_otp(db, payload.mobile)

    return {
        "status": 200,
        "message": "OTP sent successfully",
        "data": {
            "mobile": otp_entry.mobile,
        }
    }


@router.post("/verify-otp", response_model=APIResponse[OTPResponse | None])
def verify_mobile_otp(
    payload: MobileOTPVerifyRequest,
    db: Session = Depends(get_db)
):
    result = verify_otp(db, payload.mobile, payload.otp)

    if not result:
        return {
            "status": 404,
            "message": "Customer not found. Please register first.",
            "data": None
        }

    return {
        "status": 200,
        "message": "Login successful",
        "data": {
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": result["token_type"],
            "customer": result["customer"]
        }
    }

