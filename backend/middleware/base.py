from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.middleware.auth import AuthMiddleware
from backend.middleware.stats import StatsMiddleware

def include_middleware(app):
    stats = StatsMiddleware(app)
    auth = AuthMiddleware(app)
    
    app.add_middleware(BaseHTTPMiddleware, dispatch=auth)
    app.add_middleware(BaseHTTPMiddleware, dispatch=stats)
    app.add_middleware(CORSMiddleware, allow_origins=get_settings().CORS_ALLOWED_ORIGINS.split(','), allow_credentials=True, allow_methods=get_settings().CORS_ALLOWED_METHODS.split(','), allow_headers=get_settings().CORS_ALLOWED_HEADERS.split(','))