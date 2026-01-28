from pydantic import BaseModel, EmailStr, field_validator

class WebRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    contact: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return v.strip()

    @field_validator("contact")
    @classmethod
    def validate_contact(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError("Invalid contact number")
        return v
