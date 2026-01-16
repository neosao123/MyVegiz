

# DATABASE_URL = "postgresql://postgres:password@localhost:5432/mydb"




DATABASE_URL = "postgresql://postgres:root@localhost:5432/MyVegiz"





from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()

