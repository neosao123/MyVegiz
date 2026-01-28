from fastapi import APIRouter
from app.api.v1.web.routes import auth,web_slider

router = APIRouter(prefix="/web", tags=["Web"])

router.include_router(auth.router, prefix="/auth")
router.include_router(web_slider.router, prefix="/web_slider")

