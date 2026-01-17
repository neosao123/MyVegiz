from fastapi import FastAPI
from app.admin.routes import admin_router
# FastAPI is the main application class


# -Creates FastAPI app instance
# -Metadata used by:
    # Swagger UI (/docs)
    # ReDoc (/redoc)



from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError


from app.core.exceptions import AppException
from app.api.v1.router import api_router

from app.models import user,category,product,uom # noqa

import app.core.cloudinary  # noqa



app = FastAPI(title="MyVegiz API")


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=200,  # ALWAYS 200
        content={
            "status": exc.status,
            "message": exc.message,
            "data": None
        }
    )


# Handle Pydantic validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    # message = first_error.get("msg", "Validation error")

    error = exc.errors()[0]
    field = error["loc"][-1]
    error_type = error["type"]

    if error_type == "missing":
        message = f"{field.capitalize()} is required"
    else:
        message = error.get("msg", "Validation error")


    # Remove "Value error," prefix
    if message.lower().startswith("value error"):
        message = message.split(",", 1)[1].strip()

    return JSONResponse(
        status_code=200,  # ALWAYS 200 (as per your design)
        content={
            "status": 400,
            "message": message,
            "data": None
        }
    )



@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(
    request: Request,
    exc: ValidationError
):
    error = exc.errors()[0]
    field = error["loc"][-1]
    message = error.get("msg", "Validation error")

    # Clean "Value error," prefix
    if message.lower().startswith("value error"):
        message = message.split(",", 1)[1].strip()

    return JSONResponse(
        status_code=200,
        content={
            "status": 400,
            "message": message,
            "data": None
        }
    )


# Create tables (DEV only)
# Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")