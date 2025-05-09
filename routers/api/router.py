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

router = APIRouter(tags=["api"], prefix="/api")

templates = Jinja2Templates(directory="templates")

@router.get(
    "/services",
    # response_model=List[api_schemas.Service]
)
def get_servizi(language_code: str = "it"):
    data = api_service.load_data(language_code)
    return data


@router.get("/card-template", response_class=HTMLResponse)
def render_card(
    request: Request,
    name: str = Query(...),
    lat: float = Query(...),
    lon: float = Query(...),
    tipo: str = Query(...),
    info: str = Query(...),
    address: str = Query(...),
    phone: str = Query(...),
    view: str = Query("list"),
    lang: str = Query("it"),
    # distance: float = Query(None)
):
    template_name = "partials/list-card2.html" if view == "list" else "partials/popup-card2.html"
    return templates.TemplateResponse(template_name, {
        "request": request,
        "lat": lat,
        "lon": lon,
        "tipo": tipo,
        "name": name,
        "info": info,
        "address": address,
        "phone": phone,
        "translations": utils.open_language(lang),
        "lang": lang,
        # "distance": distance,
        "google_api_key": os.environ.get("GOOGLE_API_KEY"),
    })


@router.get("/autocomplete")
def autocomplete(query: str = Query(..., min_length=2)):
    try:
        response = requests.get("https://nominatim.openstreetmap.org/search", params={
            "q": f"{query}, Roma",
            "format": "json",
            "addressdetails": 1,
            "limit": 5
        }, headers={"User-Agent": "guida-dove-app/1.0"})

        response.raise_for_status()
        data = response.json()

        # Filtra lato server per sicurezza
        filtered = [item for item in data if 
                    item.get("address", {}).get("city", "").lower() == "roma" or
                    "roma" in item.get("display_name", "").lower()]

        return JSONResponse(content=filtered)
    except requests.RequestException as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
