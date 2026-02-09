from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.schemas.site_cms import SiteCMSForm
from app.services.site_cms_service import (
    get_cms_by_key,
    create_or_update_cms
)
from app.schemas.response import APIResponse
from app.models.user import User
from app.schemas.site_cms import (
    SiteCMSResponse,
    SiteCMSForm
)

router = APIRouter(tags=["Site CMS"])

# -------------------------------
# list SITECMS(terms, privacy, refund) 
# -------------------------------
# # Get CMS content based on page key (terms, privacy, refund)
# Requires authenticated user
@router.get("/{page_key}", response_model=APIResponse[SiteCMSResponse])
def get_cms(
    page_key: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    cms = get_cms_by_key(db, page_key)
    return {
        "status": 200,
        "message": "CMS fetched successfully",
        "data": cms
    }


# -------------------------------
# create/update SITECMS(terms, privacy, refund)  
# -------------------------------
# Create or update CMS content based on page key
# Accepts form data and requires authenticated user
@router.post("/{page_key}", response_model=APIResponse[SiteCMSResponse])
def save_cms(
    page_key: str,
    data: SiteCMSForm = Depends(SiteCMSForm.as_form),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    cms = create_or_update_cms(db, page_key, data)

    return {
        "status": 200,
        "message": "CMS saved successfully",
        "data": cms
    }
