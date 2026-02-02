

from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional, List
from datetime import datetime
import re


class ProductCreate(BaseModel):
    category_id: int
    sub_category_id: Optional[int] = None  #  OPTIONAL

    product_name: str
    product_short_name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    hsn_code: Optional[str] = None
    sku_code: Optional[str] = None
    is_active: bool = True

    @classmethod
    def as_form(
        cls,
        category_id: int = Form(...),
        sub_category_id: Optional[int] = Form(None),  #  OPTIONAL
        product_name: str = Form(...),
        product_short_name: str = Form(...),
        short_description: Optional[str] = Form(None),
        long_description: Optional[str] = Form(None),
        hsn_code: Optional[str] = Form(None),
        sku_code: Optional[str] = Form(None),
        is_active: bool = Form(True),
    ):
        return cls(
            category_id=category_id,
            sub_category_id=sub_category_id,
            product_name=product_name,
            product_short_name=product_short_name,
            short_description=short_description,
            long_description=long_description,
            hsn_code=hsn_code,
            sku_code=sku_code,
            is_active=is_active
        )

    @field_validator("product_name", "product_short_name", mode="before")
    @classmethod
    def required_fields(cls, v, info):
        if v is None or not str(v).strip():
            raise ValueError(f"{info.field_name.replace('_',' ').title()} is required")
        return v.strip()

    @field_validator("hsn_code")
    @classmethod
    def validate_hsn(cls, v):
        if v and not re.match(r"^[0-9]{4,8}$", v):
            raise ValueError("HSN code must be 4–8 digits")
        return v

    @field_validator("sku_code")
    @classmethod
    def validate_sku(cls, v):
        if v and not re.match(r"^[A-Z0-9]{3,5}-[A-Z0-9]{2,5}-[0-9]{2,5}$", v):
            raise ValueError(
                "SKU format must be like APP-FRU-001"
            )
        return v

class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    sub_category_id: Optional[int] = None
    product_name: Optional[str] = None
    product_short_name: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    hsn_code: Optional[str] = None
    sku_code: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        product_name: Optional[str] = Form(None),
        product_short_name: Optional[str] = Form(None),
        short_description: Optional[str] = Form(None),
        long_description: Optional[str] = Form(None),
        hsn_code: Optional[str] = Form(None),
        sku_code: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            product_name=product_name.strip() if product_name else None,
            product_short_name=product_short_name.strip() if product_short_name else None,
            short_description=short_description.strip() if short_description else None,
            long_description=long_description.strip() if long_description else None,
            hsn_code=hsn_code.strip() if hsn_code else None,
            sku_code=sku_code.strip() if sku_code else None,
            is_active=is_active,
        )
    
    @field_validator("hsn_code")
    @classmethod
    def validate_hsn(cls, v):
        if v is not None and not re.fullmatch(r"[0-9]{4,8}", v):
            raise ValueError("HSN code must be 4 to 8 digits")
        return v

    @field_validator("sku_code")
    @classmethod
    def validate_sku(cls, v):
        if v is not None and not re.fullmatch(
            r"[A-Z0-9]{3,5}-[A-Z0-9]{2,5}-[0-9]{2,5}", v
        ):
            raise ValueError("SKU format must be like APP-FRU-001")
        return v


class ProductImageResponse(BaseModel):
    product_image: str
    is_primary: bool

    class Config:
        orm_from_attributes = True


class CategoryResponse(BaseModel):
    id: int
    category_name: str

    class Config:
        orm_from_attributes = True


class SubCategoryResponse(BaseModel):
    id: int
    sub_category_name: str

    class Config:
        orm_from_attributes = True


class ProductResponse(BaseModel):
    uu_id: str
    # category_id: int
    # category_name: str
    # sub_category_id: Optional[int]  
    # sub_category_name: Optional[str]
    product_name: str
    product_short_name: str
    slug: str
    short_description: Optional[str]
    long_description: Optional[str]
    hsn_code: Optional[str]
    sku_code: Optional[str]
    is_active: bool
    created_at: datetime
    # ✅ NEW NESTED OBJECTS
    category: CategoryResponse
    sub_category: Optional[SubCategoryResponse]

    images: List[ProductImageResponse]

    class Config:
        orm_from_attributes = True



class CategoryDropdownResponse(BaseModel):
    id: int
    uu_id: str
    category_name: str

    class Config:
        orm_from_attributes = True



class SubCategoryDropdownResponse(BaseModel):
    id: int
    category_id: int 
    sub_category_name: str

    class Config:
        orm_from_attributes = True


