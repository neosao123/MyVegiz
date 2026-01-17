from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.models.user import User
from app.core.exceptions import AppException
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM
)

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(
        User.email == email,
        User.is_active == True,
        User.is_delete == False
    ).first()

    
    if not user:
        raise AppException(status=404, message="Email not registered")

    #  Password incorrect
    if not verify_password(password, user.password):
        raise AppException(status=401, message="Incorrect password")

    payload = {
        "user_id": user.id,
        "email": user.email,
    }

    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
        "token_type": "bearer"
    }



def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise AppException(status=401, message="Invalid refresh token")

        return {
            "access_token": create_access_token({
                "user_id": payload["user_id"],
                "email": payload["email"],
            }),
            "token_type": "bearer"
        }

    except JWTError:
        raise AppException(status=401, message="Refresh token expired or invalid")

