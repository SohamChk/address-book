from json.decoder import JSONDecodeError

from fastapi import APIRouter 
from fastapi import Request
from fastapi.responses import JSONResponse

from accounts.validators import RegsterUserValidator
from accounts.validators import LoginUserValidator
from accounts.serializers import RegisterUserSerializer
from accounts.serializers import LoginUserSerializer
from backend.log import log
from backend.log import log_dict
from backend.status_codes import codes

router = APIRouter(
    prefix="/api/v1/accounts",
    tags=['Accounts']
)

@router.post('/register')
async def register(request: Request, payload: RegsterUserValidator):
    extra_dict = log_dict.copy()
    extra_dict['request_id'] = request.state.request_id
    extra_dict['endpoint'] = request.scope['path']

    request_data = await request.json()
    
    log.info(f'''Request received to register user extra={str(extra_dict)}''')

    serializer = RegisterUserSerializer( attrs=request_data, extra=extra_dict )
    data = await serializer.validate()

    response = codes[201].copy()
    response['message'] = f'User registered successfully'
    log.info(f'''Request to register user completed successfully extra={str(extra_dict)}''')
    return JSONResponse(content=response, status_code=201)

@router.post('/login')
async def login(request: Request, payload: LoginUserValidator):
    extra_dict = log_dict.copy()
    extra_dict['request_id'] = request.state.request_id
    extra_dict['endpoint'] = request.scope['path']

    request_data = await request.json()
    
    log.info(f'''Request received to login user extra={str(extra_dict)}''')

    serializer = LoginUserSerializer( attrs=request_data, extra=extra_dict )
    data = await serializer.validate()

    response = codes[200].copy()
    response['message'] = f'User logged in successfully'
    response['details'] = data['details']
    log.info(f'''Request to login user completed successfully extra={str(extra_dict)}''')
    return JSONResponse(content=response, status_code=200)