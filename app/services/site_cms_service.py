from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.site_cms import SiteCMS
from app.core.exceptions import AppException

# Allowed CMS page keys
VALID_KEYS = ["terms", "privacy", "refund"]

# =========================================================
# Fetch CMS content by page key (terms, privacy, refund)
# =========================================================
def get_cms_by_key(db: Session, page_key: str):
    if page_key not in VALID_KEYS:
        raise AppException(400, "Invalid page key")

    return db.query(SiteCMS).filter(
        SiteCMS.page_key == page_key,
        SiteCMS.is_delete == False
    ).first()


# =========================================================
# Create/Update CMS
# =========================================================
# Create a new CMS record or update existing one based on page_key
# If record exists → update fields
# If record does not exist → create new entry
def create_or_update_cms(
    db: Session,
    page_key: str,
    data
):
    if page_key not in VALID_KEYS:
        raise AppException(400, "Invalid page key")

    cms = get_cms_by_key(db, page_key)

    if cms:
        # UPDATE
        for field, value in data.dict(exclude_unset=True).items():
            setattr(cms, field, value)

        cms.is_update = True
        cms.updated_at = func.now()

    else:
        # CREATE (first time only)
        cms = SiteCMS(
            page_key=page_key,
            **data.dict()
        )
        db.add(cms)

    db.commit()
    db.refresh(cms)
    return cms
