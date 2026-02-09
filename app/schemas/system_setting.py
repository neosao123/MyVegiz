from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional
from typing import Any
from datetime import datetime

# =========================================================
# SYSTEM SETTINGS FORM (INPUT)
# ---------------------------------------------------------
# Used by Admin frontend to submit ALL system settings
# in a single form (multipart/form-data).

# First submission → creates records
# Next submissions → updates existing records
# =========================================================
class SystemSettingForm(BaseModel):
    # Maintenance
    app_maintenance: bool = False

    # Android
    playstore_version: str
    playstore_forceupdate: bool = False
    playstore_updatemessage: Optional[str] = None

    # iOS
    ios_version: str
    ios_forceupdate: bool = False
    ios_updatemessage: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        app_maintenance: bool = Form(False),

        playstore_version: str = Form(...),
        playstore_forceupdate: bool = Form(False),
        playstore_updatemessage: Optional[str] = Form(None),

        ios_version: str = Form(...),
        ios_forceupdate: bool = Form(False),
        ios_updatemessage: Optional[str] = Form(None),
    ):
        return cls(
            app_maintenance=app_maintenance,
            playstore_version=playstore_version.strip(),
            playstore_forceupdate=playstore_forceupdate,
            playstore_updatemessage=playstore_updatemessage.strip() if playstore_updatemessage else None,
            ios_version=ios_version.strip(),
            ios_forceupdate=ios_forceupdate,
            ios_updatemessage=ios_updatemessage.strip() if ios_updatemessage else None,
        )

    @field_validator("playstore_version", "ios_version")
    @classmethod
    def version_required(cls, v):
        if not v:
            raise ValueError("Version is required")
        return v


# =========================================================
# SYSTEM SETTINGS RESPONSE (OUTPUT)
# =========================================================
class SystemSettingResponse(BaseModel):
    setting_key: str
    title: str | None
    value: Any
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        orm_from_attributes = True
