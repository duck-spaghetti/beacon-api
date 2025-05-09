from fastapi import APIRouter, Query
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from pathlib import Path
from routers.web import (
    service as web_service,
    schemas as web_schemas
)
import json
import utils

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="templates")


@router.get("/{lang}", response_class=HTMLResponse)
async def home(request: Request, lang: str):
    translations = utils.open_language(lang)
    if lang == "ar":
        dir = "rtl"
    else:
        dir = "ltr"
    return templates.TemplateResponse("home.html", {
        "request": request,
        "translations": translations,
        "lang": lang,
        "dir": dir,
    })