from fastapi import APIRouter
from app.api.v1.web.routes import auth,web_categories,web_products
from app.api.v1.web.routes import auth,web_slider

router = APIRouter(prefix="/web", tags=["Web"])

router.include_router(auth.router, prefix="/auth")
router.include_router(
    web_categories.router,
    prefix="/categories")


router.include_router(
    web_products.router,
    prefix="/products",
)
router.include_router(web_slider.router, prefix="/web_slider")

