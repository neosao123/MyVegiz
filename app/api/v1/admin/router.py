from fastapi import APIRouter

# -------------------------------------------------
# ADMIN ROUTE IMPORTS
# Each module handles a specific admin feature
# -------------------------------------------------
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
    slider,
    coupon_code
)

# -------------------------
# BASE Admin ROUTER
# -------------------------
router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# USER ROUTES
router.include_router(users.router, prefix="/users")

# AUTH ROUTES
router.include_router(auth.router, prefix="/auth")

# CATEGORY ROUTES
router.include_router(categories.router, prefix="/categories")

# PRODUCT ROUTES
router.include_router(products.router, prefix="/products")

# UOM ROUTES
router.include_router(uoms.router, prefix="/uoms")

# Email-setting ROUTES
router.include_router(email_settings.router, prefix="/email-settings")

# MAIN CATEGORY ROUTES
router.include_router(main_categories.router, prefix="/main-categories")

# SUB CATEGORY ROUTES
router.include_router(sub_categories.router, prefix="/sub-categories")

# Zone ROUTES
router.include_router(zones.router, prefix="/zone")

# Product Variants ROUTES
router.include_router(product_variants.router, prefix="/product-variants")

# Profile Update ROUTES
router.include_router(profile_update.router, prefix="/users", tags=["Users"])

# Slider ROUTES
router.include_router(slider.router, prefix="/slider")

# Coupon Code ROUTES
router.include_router(coupon_code.router, prefix="/coupon_code")

