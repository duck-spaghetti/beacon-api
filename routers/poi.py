from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel

from database.database import Database
import os


API_KEY = os.getenv("API_KEY", "secret")


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
        )


db = Database()
router = APIRouter(
    tags=["POI"],
    prefix="/poi",
    # dependencies=[Depends(verify_api_key)]
)


class POIBase(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    transport: Optional[str] = None
    is_active: bool = True
    name: Optional[str] = None
    info_it: Optional[str] = None
    info_en: Optional[str] = None
    info_ar: Optional[str] = None
    time_table: Optional[str] = None
    type: Optional[str] = None


class POICreate(POIBase):
    pass


class POIUpdate(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    transport: Optional[str] = None
    is_active: Optional[bool] = None
    name: Optional[str] = None
    info_it: Optional[str] = None
    info_en: Optional[str] = None
    info_ar: Optional[str] = None
    time_table: Optional[str] = None
    type: Optional[str] = None


class POI(POIBase):
    id: int


@router.get("/", response_model=List[POI])
def list_pois():
    rows = db.execute_query("SELECT * FROM poi")
    return [POI(**dict(row)) for row in rows]


@router.get("/{poi_id}", response_model=POI)
def get_poi(poi_id: int):
    row = db.get_poi_by_id(poi_id)
    if not row:
        raise HTTPException(status_code=404, detail="POI not found")
    return row


@router.post("/", response_model=POI)
def create_poi(poi: POICreate):
    poi_id = db.insert_poi(poi.dict())
    return {"id": poi_id, **poi.dict()}


@router.put("/{poi_id}", response_model=POI)
def update_poi(poi_id: int, poi: POIUpdate):
    existing = db.get_poi_by_id(poi_id)
    if not existing:
        raise HTTPException(status_code=404, detail="POI not found")
    update_data = {k: v for k, v in poi.dict(exclude_none=True).items()}
    db.update_poi(poi_id, update_data)
    return db.get_poi_by_id(poi_id)


@router.delete("/{poi_id}")
def delete_poi(poi_id: int):
    existing = db.get_poi_by_id(poi_id)
    if not existing:
        raise HTTPException(status_code=404, detail="POI not found")
    db.delete_poi(poi_id)
    return {"status": "deleted"}

