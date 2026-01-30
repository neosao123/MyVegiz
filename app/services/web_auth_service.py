from sqlalchemy.orm import Session
import uuid

from app.models.customer import Customer
from app.core.exceptions import AppException
from app.core.security import create_access_token, create_refresh_token


def register_customer_send_otp(db: Session, data):
    # check email
    # existing_email = db.query(Customer).filter(
    #     Customer.email == data.email,
    #     Customer.is_delete == False
    # ).first()

    # if existing_email and existing_email.is_active:
    #     raise AppException(status=400, message="Email already exists")

    # check contact
    existing_customer = db.query(Customer).filter(
        Customer.contact == data.contact,
        Customer.is_delete == False
    ).first()

    # 🔴 CASE 1: ACTIVE user → BLOCK
    if existing_customer and existing_customer.is_active:
        raise AppException(status=400, message="Contact already exists")

    # 🟡 CASE 2: INACTIVE user → RESEND OTP
    if existing_customer and not existing_customer.is_active:
        otp_entry = send_otp(db, data.contact)
        return {
            "mobile": otp_entry.mobile,
            "message": "OTP resent successfully"
        }

    # 🟢 CASE 3: NEW user → CREATE + SEND OTP
    customer = Customer(
        uu_id=str(uuid.uuid4()),
        name=data.name,
        # email=data.email,
        contact=data.contact,
        is_active=False
    )

    db.add(customer)
    db.commit()

    otp_entry = send_otp(db, data.contact)

    return {
        "mobile": otp_entry.mobile,
        "message": "OTP sent successfully"
    }


def verify_otp_and_login(db: Session, mobile: str, otp: str):
    now = datetime.now(timezone.utc)

    otp_entry = db.query(MobileOTP).filter(
        MobileOTP.mobile == mobile,
        MobileOTP.expires_at > now
    ).order_by(MobileOTP.created_at.desc()).first()

    if not otp_entry:
        raise AppException(status=404, message="OTP not requested")

    if otp_entry.otp != otp:
        raise AppException(status=401, message="Invalid OTP")

    # delete OTP
    db.delete(otp_entry)

    customer = db.query(Customer).filter(
        Customer.contact == mobile,
        Customer.is_delete == False
    ).first()

    if not customer:
        raise AppException(status=404, message="Customer not found")

    # activate customer
    customer.is_active = True
    db.commit()
    db.refresh(customer)

    payload = {
        "customer_id": customer.id,
        "mobile": customer.contact,
        "type": "access"
    }

    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
        "token_type": "bearer",
        "customer": customer
    }



from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.models.otp import MobileOTP

DEFAULT_OTP = "123456"
OTP_EXPIRY_MINUTES = 10


def send_otp(db: Session, mobile: str):
    now = datetime.now(timezone.utc)

    # 🔍 STEP 1: Check for existing unverified & unexpired OTP
    existing_otp = (
        db.query(MobileOTP)
        .filter(
            MobileOTP.mobile == mobile,
            MobileOTP.is_verified == False,
            MobileOTP.expires_at > now
        )
        .order_by(MobileOTP.created_at.desc())
        .first()
    )

    #  STEP 2: If valid OTP exists → reuse it
    if existing_otp:
        return existing_otp

    # 🔴 STEP 3: Delete expired OTPs
    db.query(MobileOTP).filter(
        MobileOTP.mobile == mobile,
        MobileOTP.expires_at <= now
    ).delete(synchronize_session=False)

    # 🔴 STEP 4: Create new OTP
    otp_entry = MobileOTP(
        mobile=mobile,
        otp=DEFAULT_OTP,
        expires_at=now + timedelta(minutes=OTP_EXPIRY_MINUTES)
    )

    db.add(otp_entry)
    db.commit()
    db.refresh(otp_entry)

    return otp_entry


def verify_otp(db: Session, mobile: str, otp: str):
    now = datetime.now(timezone.utc)
    otp_entry = (
        db.query(MobileOTP)
        .filter(
            MobileOTP.mobile == mobile,
            MobileOTP.expires_at > now
        )
        .order_by(MobileOTP.created_at.desc())
        .first()
    )

    if not otp_entry:
        raise AppException(status=404, message="OTP not requested. Please request OTP first.")

    if otp_entry.expires_at < datetime.now(timezone.utc):
        raise AppException(status=401, message="OTP expired. Please request a new one.")

    if otp_entry.otp != otp:
        raise AppException(status=401, message="Incorrect OTP.")

    db.delete(otp_entry)
    db.commit()

    customer = db.query(Customer).filter(
        Customer.contact == mobile,
        Customer.is_active == True,
        Customer.is_delete == False
    ).first()

    if not customer:
        return None  # register first

    access_payload = {
        "customer_id": customer.id,
        "mobile": customer.contact,
        "type": "access"
    }

    refresh_payload = {
        "customer_id": customer.id,
        "mobile": customer.contact,
        "type": "refresh"
    }

    return {
        "access_token": create_access_token(access_payload),
        "refresh_token": create_refresh_token(refresh_payload),
        "token_type": "bearer",
        "customer": customer
    }
