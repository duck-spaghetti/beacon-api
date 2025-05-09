from fastapi import APIRouter, Query
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from routers.api import (
    service as api_service,
    schemas as api_schemas
)
from typing import List
import os
import requests
from fastapi.responses import JSONResponse
import utils

router = APIRouter(tags=["POI"], prefix="/poi")

@router.get(
    "/",
)
def get_servizi():
    return None