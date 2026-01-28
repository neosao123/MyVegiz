from fastapi import APIRouter

from app.api.v1.admin.router import router as admin_router
from app.api.v1.web.router import router as web_router

api_router = APIRouter()

api_router.include_router(admin_router)
api_router.include_router(web_router)

