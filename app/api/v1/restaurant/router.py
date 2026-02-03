from fastapi import APIRouter
from app.api.v1.restaurant.routes import entity_category

router = APIRouter(prefix="/restaurant", tags=["Restaurant"])

router.include_router(entity_category.router, prefix="/entitycategory")


