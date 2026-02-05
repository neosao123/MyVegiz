from fastapi import APIRouter
from app.api.v1.restaurant.routes import entity_category
from app.api.v1.restaurant.routes import menu_category

# -------------------------
# ROUTE IMPORTS
# -------------------------
from app.api.v1.restaurant.routes import entity_category,menu,menu_item


# -------------------------
# BASE RESTAURANT ROUTER
# -------------------------
router = APIRouter(prefix="/restaurant", tags=["Restaurant"])



# ENTITY CATEGORY ROUTES
router.include_router(entity_category.router, prefix="/entitycategory")

# MENU ROUTES
router.include_router(menu.router, prefix="/menu")

# MENU ITEM ROUTES
router.include_router(menu_item.router, prefix="/menuitem")

# MENU CATEGORY ROUTES
router.include_router(menu_category.router, prefix="/menucategory")

