import os
from pathlib import Path
from functools import lru_cache

from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ADRESS BOOK SERVICE"
    PROJECT_VERSION: str = "DAY=20230429.RELEASE=1"

    DEBUG: int = os.environ.get("DEBUG").strip()

    GEOLOC_API_KEY: str = os.environ.get('GEOLOC_API_KEY').strip()
    SPATIALITE_PATH: str = os.environ.get('SPATIALITE_PATH').strip()

    SECRET_KEY: str = os.environ.get("SECRET_KEY").strip() 
    ALGORITHM: str = "HS256"    # Hashing algorithm for JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # in mins

    # No JWT header will be checked for these APIs
    NON_AUTH_ENDPOINTS: str = os.environ.get("NON_AUTH_APIS")

    # Database settings
    DB_FILE: str = os.environ.get("DB_FILE").strip()
    DATABASE_URL: str = f'''sqlite:///{DB_FILE}'''

    # CORS settings
    CORS_ALLOWED_ORIGINS: str = os.environ.get("CORS_ALLOWED_ORIGINS").strip()
    CORS_ALLOWED_METHODS: str = os.environ.get("CORS_ALLOWED_METHODS").strip()
    CORS_ALLOWED_HEADERS: str = os.environ.get("CORS_ALLOWED_HEADERS").strip()

@lru_cache()
def get_settings():
    return Settings()