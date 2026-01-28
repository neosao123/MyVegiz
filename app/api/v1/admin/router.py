from fastapi import APIRouter

from app.api.v1.admin.routes import (
    users,
    auth,
    categories,
    products,
    uoms,
    email_settings,
    main_categories,
    sub_categories,
    zones,
    product_variants,
    profile_update,
    slider
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

router.include_router(users.router, prefix="/users")
router.include_router(auth.router, prefix="/auth")
router.include_router(categories.router, prefix="/categories")
router.include_router(products.router, prefix="/products")
router.include_router(uoms.router, prefix="/uoms")
router.include_router(email_settings.router, prefix="/email-settings")
router.include_router(main_categories.router, prefix="/main-categories")
router.include_router(sub_categories.router, prefix="/sub-categories")
router.include_router(zones.router, prefix="/zone")
router.include_router(product_variants.router, prefix="/product-variants")
router.include_router(profile_update.router, prefix="/users", tags=["Users"])
router.include_router(slider.router, prefix="/slider")
