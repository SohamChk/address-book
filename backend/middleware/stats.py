import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from backend.log import log, log_dict

class StatsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def __call__(self, request: Request, call_next):
        start_time = time.time()
        request_id = uuid.uuid4()

        extra_dict = log_dict.copy()
        extra_dict['request_id'] = str(request_id)
        extra_dict['endpoint'] = str(request.scope['path'])

        request.state.request_id = request_id
        response = await call_next(request)
        
        process_time = time.time() - start_time
        log.info(f'''STATISTICS: DURATION={ str(process_time) } seconds extra={str(extra_dict)}''')
        response.headers["X-Response-Duration"] = str(process_time)
        response.headers["X-Thread-ID"] = str(request_id)
        return response