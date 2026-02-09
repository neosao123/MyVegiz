import json
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.system_setting import SystemSetting

# =========================================================
# UPSERT HELPER
# ---------------------------------------------------------
# Creates a new system setting if it does not exist,
# otherwise updates the existing one.
#
# This ensures:
# - First save → INSERT
# - Next saves → UPDATE
#
# Used internally by save_system_settings()
# =========================================================
def upsert_setting(
    db: Session,
    key: str,
    title: str,
    value
):
    setting = db.query(SystemSetting).filter(
        SystemSetting.setting_key == key,
        SystemSetting.is_delete == False
    ).first()

    if setting:
        setting.value = value
        setting.is_update = True
        setting.updated_at = func.now()
    else:
        setting = SystemSetting(
            setting_key=key,
            title=title,
            value=value
        )
        db.add(setting)

    return setting



# =========================================================
# SERIALIZER
# ---------------------------------------------------------
# Converts DB record into frontend-friendly response
#
# Handles:
# - maintenance_mode → int (0 / 1)
# - android / ios settings → parsed JSON object
#
# Used by:
# - save_system_settings()
# - list_system_settings()
# =========================================================
def serialize_setting(s: SystemSetting):
    value = s.value

    # JSON fields (android / ios)
    try:
        value = json.loads(s.value)
    except Exception:
        # maintenance_mode
        if s.setting_key == "maintenance_mode":
            value = int(s.value)

    return {
        "setting_key": s.setting_key,
        "title": s.title,
        "value": value,
        "is_active": s.is_active,
        "created_at": s.created_at,
        "updated_at": s.updated_at,
    }



# =========================================================
# SAVE / UPDATE SYSTEM SETTINGS
# ---------------------------------------------------------
# Accepts data from a single frontend form and:
# - Saves maintenance mode
# - Saves Android app version config
# - Saves iOS app version config
#
# Always returns response in SAME format as list API
# =========================================================
def save_system_settings(db: Session, data):
    settings = []

    # Maintenance
    settings.append(
        upsert_setting(
            db,
            key="maintenance_mode",
            title="Maintenance Mode",
            value="1" if data.app_maintenance else "0"
        )
    )

    # Android
    settings.append(
        upsert_setting(
            db,
            key="android_app_version",
            title="Android App Version",
            value=json.dumps({
                "version": data.playstore_version,
                "force_update": data.playstore_forceupdate,
                "update_message": data.playstore_updatemessage
            })
        )
    )

    # iOS
    settings.append(
        upsert_setting(
            db,
            key="ios_app_version",
            title="iOS App Version",
            value=json.dumps({
                "version": data.ios_version,
                "force_update": data.ios_forceupdate,
                "update_message": data.ios_updatemessage
            })
        )
    )

    db.commit()

    for s in settings:
        db.refresh(s)

    return [serialize_setting(s) for s in settings]



# =========================================================
# LIST SYSTEM SETTINGS
# ---------------------------------------------------------
# Fetches all active system settings and returns them
# in frontend-ready format.
# =========================================================
def list_system_settings(db: Session):
    settings = db.query(SystemSetting).filter(
        SystemSetting.is_delete == False,
        SystemSetting.is_active == True
    ).order_by(SystemSetting.id.asc()).all()

    return [serialize_setting(s) for s in settings]