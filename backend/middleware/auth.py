# Standard library imports
import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt

from backend.config import get_settings
from backend.log import log, log_dict
from backend.status_codes import codes

async def get_client_from_token(token: str):
    try:
        payload = jwt.decode( token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM] )
        email = payload.get('email', None)

        if email is None:
            return None
        
        return email
    except JWTError as e:
        log.error(str(e))
        return None

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        self.non_auth_endpoints  = set(get_settings().NON_AUTH_ENDPOINTS.split(','))
        super().__init__(app)

    async def __call__(self, request: Request, call_next):
        start_time = time.time()
        if request.scope['path'] not in self.non_auth_endpoints:
            token = request.headers.get('authorization', None)
            if token:
                email = await get_client_from_token(token.split()[-1])
                if not email:
                    response = codes[401].copy()
                    response['message'] = 'Authorization failed'
                    return JSONResponse(content=response, status_code=401)
                
                request.state.user = email
            else:
                response = codes[401].copy()
                response['message'] = 'No authorization token provided.'
                return JSONResponse(content=response, status_code=401)
            
        process_time = time.time() - start_time
        response = await call_next(request)
        response.headers["X-Auth-Duration"] = str(process_time)
            
        return response