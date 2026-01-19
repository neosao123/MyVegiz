from fastapi import APIRouter
from app.api.v1.routes.users import router as user_router
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.categories import router as category_router
from app.api.v1.routes.products import router as product_router
from app.api.v1.routes.uoms import router as uom_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(category_router,prefix="/categories",tags=["Categories"])
api_router.include_router(product_router,prefix="/products",tags=["Products"])
api_router.include_router(uom_router,prefix="/uoms",tags=["UOMs"])