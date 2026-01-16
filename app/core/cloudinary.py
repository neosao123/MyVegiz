import cloudinary
import cloudinary.uploader
import cloudinary.api
from app.core.config import settings  # or env vars

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

