from fastapi import APIRouter

# APIRouter= Group related APIs together

admin_router = APIRouter()

@admin_router.get("/health")
def admin_health_check():
    return {
        "status": "success",
        "message": "MyVegiz Admin API is running 🚀"
    }
