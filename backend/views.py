# Related third-party imports
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from backend.status_codes import codes
from backend.config import get_settings
from backend.log import log

router = APIRouter(
    prefix='',
    tags=['Base']
)

@router.get("/version")
async def version(key: str = None):
    settings = get_settings()

    response = dict()
    response['name'] = settings.PROJECT_NAME
    response['version'] = settings.PROJECT_VERSION
    response['environment'] = "DEVELOPMENT" if int(settings.DEBUG) else "PRODUCTION"
    response['status'] = 'UP'
    log.info(" ".join(['Inside the get version function']))
    return JSONResponse(content=response)
