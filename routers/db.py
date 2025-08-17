from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
import os
from pathlib import Path

API_KEY = os.getenv("API_KEY", "secret")

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "poi.db"

router = APIRouter(tags=["db"])

@router.get("/{api_key}-db")
def serve_db(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
        )
    return FileResponse(str(DB_PATH), media_type="application/octet-stream", filename="poi.db")
