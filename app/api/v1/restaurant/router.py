from fastapi import APIRouter
from app.api.v1.restaurant.routes import entity_category
from app.api.v1.restaurant.routes import menu_category
from app.api.v1.restaurant.routes import entity_category,menu,menu_item

router = APIRouter(prefix="/restaurant", tags=["Restaurant"])

router.include_router(entity_category.router, prefix="/entitycategory")
router.include_router(menu.router, prefix="/menu")
router.include_router(menu_item.router, prefix="/menuitem")


router.include_router(menu_category.router, prefix="/menucategory")

