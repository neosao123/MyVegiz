from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.email_setting import EmailSetting
from app.schemas.email_settings import EmailSettingCreate, TestEmailRequest
from app.core.exceptions import AppException
from app.core.mailer import send_email

# =========================================================
# GET EMAIL SETTINGS
# =========================================================
def get_email_settings(db: Session):
    return db.query(EmailSetting).first()

# =========================================================
# CREATE EMAIL SETTINGS (ONE-TIME SETUP)
# =========================================================
def create_email_settings(db: Session, data: EmailSettingCreate):
    existing = db.query(EmailSetting).first()

    if existing:
        raise AppException(
            status=400,
            message="Email settings already exist. Use update."
        )

    settings = EmailSetting(**data.model_dump())

    try:
        db.add(settings)
        db.commit()
        db.refresh(settings)
        return settings
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error")

# =========================================================
# UPDATE EMAIL SETTINGS
# =========================================================
def update_email_settings(db: Session, data: EmailSettingCreate):
    settings = db.query(EmailSetting).first()

    if not settings:
        raise AppException(status=404, message="Email settings not found")

    for key, value in data.model_dump().items():
        setattr(settings, key, value)

    settings.is_update = True

    try:
        db.commit()
        db.refresh(settings)
        return settings
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error")


# =========================================================
# SEND TEST EMAIL
# =========================================================
def send_test_email(db: Session, payload: TestEmailRequest):
    settings = db.query(EmailSetting).first()

    if not settings:
        raise AppException(status=404, message="Email settings not found")

    try:
        send_email(
            host=settings.host,
            port=settings.port,
            username=settings.username,
            password=settings.password,
            encryption=settings.encryption,
            from_name=settings.from_name,
            from_email=settings.from_email,
            to_email=payload.to_email,
            subject=payload.subject,
            message=payload.message,
        )
        return True

    except Exception as e:
        raise AppException(
            status=500,
            message=f"Failed to send email: {str(e)}"
        )
