from pydantic import BaseModel, field_validator
from fastapi import Form
from typing import Optional, List, Dict
from datetime import datetime
import json

# =========================================================
# ZONE CREATE SCHEMA
# Used to create a delivery/service zone
# - Accepts polygon as JSON string via form-data
# - Validates polygon structure & uniqueness
# =========================================================
class ZoneCreate(BaseModel):
    zone_name: str
    city: str
    state: str
    polygon: List[Dict[str, float]]
    is_deliverable: bool = False
    is_active: bool = True

    @classmethod
    def as_form(
        cls,
        zone_name: str = Form(...),
        city: str = Form(...),
        state: str = Form(...),
        polygon: str = Form(...),
        is_deliverable: bool = Form(False),
        is_active: bool = Form(True),
    ):
        return cls(
            zone_name=zone_name.strip(),
            city=city.strip(),
            state=state.strip(),
            polygon=json.loads(polygon),
            is_deliverable=is_deliverable,
            is_active=is_active,
        )
    
    # -----------------------------------------------------
    # POLYGON VALIDATION
    # - Minimum 5 points
    # - Each point must contain lat & lng
    # - No duplicate coordinates allowed
    # -----------------------------------------------------
    @field_validator("polygon")
    @classmethod
    def validate_polygon(cls, v):
        if not v or len(v) < 5:
            raise ValueError("Polygon must have at least 5 points")

        seen = set()
        for p in v:
            if "lat" not in p or "lng" not in p:
                raise ValueError("Each point must contain lat & lng")

            key = (p["lat"], p["lng"])
            if key in seen:
                raise ValueError("Duplicate lat/lng points are not allowed in polygon")
            seen.add(key)

        return v



# =========================================================
# ZONE UPDATE SCHEMA
# Used for partial updates
# - All fields optional
# - Polygon validation only runs if provided
# =========================================================
class ZoneUpdate(BaseModel):
    zone_name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    polygon: Optional[List[Dict[str, float]]] = None
    is_deliverable: Optional[bool] = None
    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        zone_name: Optional[str] = Form(None),
        city: Optional[str] = Form(None),
        state: Optional[str] = Form(None),
        polygon: Optional[str] = Form(None),
        is_deliverable: Optional[bool] = Form(None),
        is_active: Optional[bool] = Form(None),
    ):
        return cls(
            zone_name=zone_name.strip() if zone_name else None,
            city=city.strip() if city else None,
            state=state.strip() if state else None,
            polygon=json.loads(polygon) if polygon else None,
            is_deliverable=is_deliverable,
            is_active=is_active,
        )
    
        
    @field_validator("polygon")
    @classmethod
    def validate_polygon(cls, v):
        # ✅ If polygon is not provided → skip validation
        if v is None:
            return v

        if len(v) < 5:
            raise ValueError("Polygon must have at least 5 points")

        seen = set()
        for p in v:
            if "lat" not in p or "lng" not in p:
                raise ValueError("Each point must contain lat & lng")

            key = (p["lat"], p["lng"])
            if key in seen:
                raise ValueError("Duplicate lat/lng points are not allowed in polygon")
            seen.add(key)

        return v


# =========================================================
# ZONE RESPONSE SCHEMA
# Used when returning full zone details
# =========================================================
class ZoneResponse(BaseModel):
    id: int
    zone_name: str
    city: str
    state: str
    polygon: List[Dict[str, float]]
    is_deliverable: bool
    is_active: bool
    created_at: datetime

    class Config:
        orm_from_attributes = True

# =========================================================
# ZONE POLYGON RESPONSE
# Lightweight response for maps / frontend drawing
# =========================================================
class ZonePolygonResponse(BaseModel):
    zone_id: int
    zone_name: str
    polygon: List[Dict[str, float]]