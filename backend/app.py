from fastapi import FastAPI

from backend.config import get_settings
from backend.routes import include_router
from backend.middleware.base import include_middleware
from backend.db.session import session

settings = get_settings()
app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
include_middleware(app)

async def start_app():
    include_router(app)
    session.init()
    session.create_all()
