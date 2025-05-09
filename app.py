from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers.api.router import router as api_router
from routers.web.router import router as web_router
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def config():
    app.include_router(api_router)
    app.include_router(web_router)

config()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
