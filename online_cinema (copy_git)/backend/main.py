import app
from fastapi import FastAPI
from .database import engine, Base
from . import models
from backend.database import engine
from backend import models
from backend.routers import movies
from backend.routers import users
from backend.routers import favorites
from backend.routers.services.config.app_config import AppConfig
from backend.routers import reports
from fastapi.staticfiles import StaticFiles
from backend.routers import recommendations
from backend.routers import reports



app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

app.include_router(recommendations.router)
app.include_router(movies.router)
app.include_router(users.router)
app.include_router(favorites.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {"message": "Online Cinema API working!"}

from backend.routers.services.config.app_config import AppConfig

@app.get("/config")
def get_config():
    cfg = AppConfig()
    return {
        "service_name": cfg.service_name,
        "default_quality": cfg.default_video_quality,
        "debug": cfg.debug,
        "version": cfg.version
    }




