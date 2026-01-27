from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.email_settings import (
    EmailSettingCreate,
    EmailSettingResponse,
    TestEmailRequest
)
from app.schemas.response import APIResponse
from app.services.email_setting_service import (
    create_email_settings,
    get_email_settings,
    update_email_settings,
    send_test_email
)

router = APIRouter(tags=["Email Settings"])


@router.post("", response_model=APIResponse[EmailSettingResponse])
def create_settings(
    payload: EmailSettingCreate = Depends(EmailSettingCreate.as_form),
    db: Session = Depends(get_db)
):
    data = create_email_settings(db, payload)
    return {
        "status": 201,
        "message": "Email settings saved",
        "data": data
    }


@router.get("", response_model=APIResponse[EmailSettingResponse])
def get_settings(db: Session = Depends(get_db)):
    data = get_email_settings(db)
    return {
        "status": 200,
        "message": "Email settings fetched",
        "data": data
    }


@router.put("", response_model=APIResponse[EmailSettingResponse])
def update_settings(
    payload: EmailSettingCreate = Depends(EmailSettingCreate.as_form),
    db: Session = Depends(get_db)
):
    data = update_email_settings(db, payload)
    return {
        "status": 200,
        "message": "Email settings updated",
        "data": data
    }


@router.post("/test")
def test_email(
    payload: TestEmailRequest = Depends(TestEmailRequest.as_form),
    db: Session = Depends(get_db)
):
    send_test_email(db, payload)
    return {
        "status": 200,
        "message": "Test email sent",
        "data": {}
    }
