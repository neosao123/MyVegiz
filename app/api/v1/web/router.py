from fastapi import APIRouter
from app.api.v1.web.routes import auth

router = APIRouter(prefix="/web", tags=["Web"])
router.include_router(auth.router, prefix="/auth")
