from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.zone import Zone
from app.schemas.zone import ZoneCreate, ZoneUpdate
from app.core.exceptions import AppException
from sqlalchemy.exc import IntegrityError
from app.utils.geo import point_in_polygon
from app.models.zone import Zone

def create_zone(db: Session, data: ZoneCreate):
    zone = Zone(
        zone_name=data.zone_name,
        city=data.city,
        state=data.state,
        polygon=data.polygon,
        is_deliverable=data.is_deliverable,
        is_active=data.is_active
    )

    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone



def list_zones(db: Session, offset: int, limit: int):
    # -------------------------------
    # Base filters (soft delete aware)
    # -------------------------------
    base_query = db.query(Zone).filter(
        Zone.is_delete == False,
        Zone.is_active == True
    ).order_by(Zone.created_at.desc())

    total_records = base_query.count()

    zones = base_query.offset(offset).limit(limit).all()

    return total_records, zones


def update_zone(db: Session, zone_id: int, data: ZoneUpdate):
    zone = db.query(Zone).filter(
        Zone.id == zone_id,
        Zone.is_delete == False
    ).first()

    if not zone:
        raise AppException(status=404, message="Zone not found")

    if data.zone_name is not None:
        zone.zone_name = data.zone_name

    if data.city is not None:
        zone.city = data.city

    if data.state is not None:
        zone.state = data.state

    if data.polygon is not None:
        zone.polygon = data.polygon

    if data.is_deliverable is not None:
        zone.is_deliverable = data.is_deliverable

    if data.is_active is not None:
        zone.is_active = data.is_active

    zone.is_update = True
    zone.updated_at = func.now()

    db.commit()
    db.refresh(zone)
    return zone


def delete_zone(db: Session, zone_id: int):
    zone = db.query(Zone).filter(
        Zone.id == zone_id,
        Zone.is_delete == False
    ).first()

    if not zone:
        raise AppException(status=404, message="Zone not found")

    zone.is_delete = True
    zone.is_active = False
    zone.deleted_at = func.now()

  
    try:
        db.commit()
        db.refresh(zone)
        return zone
    except IntegrityError:
        db.rollback()
        raise AppException(status=500, message="Database error while deleting zone")


def get_zones_by_lat_lng(db, lat: float, lng: float):
    zones = db.query(Zone).filter(
        Zone.is_delete == False,
        Zone.is_active == True
    ).all()

    matched_zones = []

    for zone in zones:
        if zone.polygon and point_in_polygon(lat, lng, zone.polygon):
            matched_zones.append(zone)

    return matched_zones