from pydantic import BaseModel
from enum import Enum


class StructureType(str, Enum):
    lavarsi = "lavarsi"
    mangiare = "mangiare"
    dormire = "dormire"
    documenti = "documenti"
    ascolto = "ascolto"
    altro = "altro"


class Service(BaseModel):
    address: str
    lat: str
    lon: str
    info: str
    phone: str
    type: StructureType
