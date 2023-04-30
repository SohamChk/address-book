from json.decoder import JSONDecodeError

from fastapi import APIRouter 
from fastapi import Request
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from address.validators import AddAddressValidator
from address.validators import UpdateAddressValidator
from address.validators import NearbyAddressValidator
from address.serializers import AddAddressSerializer
from address.serializers import ListAddressesSerializer
from address.serializers import GetNearestAddressesSerializer
from address.serializers import UpdateAddressSerializer
from address.serializers import DeleteAddressSerializer
from backend.log import log
from backend.log import log_dict
from backend.status_codes import codes

router = APIRouter(
    prefix="/api/v1/address",
    tags=['Address']
)

@router.post('/add')
async def Add(request: Request, payload: AddAddressValidator):
    extra_dict = log_dict.copy()
    extra_dict['request_id'] = request.state.request_id
    extra_dict['endpoint'] = request.scope['path']

    request_data = await request.json()
    
    log.info(f'''Request received to add address extra={str(extra_dict)}''')

    serializer = AddAddressSerializer( attrs=request_data, user=request.state.user, extra=extra_dict )
    data = await serializer.validate()

    response = codes[201].copy()
    response['message'] = f'Address added successfully'
    log.info(f'''Request to add address completed successfully extra={str(extra_dict)}''')
    return JSONResponse(content=response, status_code=201)

@router.get('/list')
async def list(request: Request):
    extra_dict = log_dict.copy()
    extra_dict['request_id'] = request.state.request_id
    extra_dict['endpoint'] = request.scope['path']
    
    log.info(f'''Request received to list addresses extra={str(extra_dict)}''')

    serializer = ListAddressesSerializer( attrs={}, user=request.state.user, extra=extra_dict )
    data = await serializer.validate()

    response = codes[200].copy()
    response['message'] = f'Address fetched successfully'
    response['details'] = data['details']
    log.info(f'''Request to list address completed successfully extra={str(extra_dict)}''')
    return JSONResponse(content=response, status_code=200)

@router.post('/get/nearest')
async def get_nearby(request: Request, payload: NearbyAddressValidator, distance: int = 5000):
    extra_dict = log_dict.copy()
    extra_dict['request_id'] = request.state.request_id
    extra_dict['endpoint'] = request.scope['path']

    request_data = await request.json()
    request_data['distance'] = distance
    
    log.info(f'''Request received to fetch nearest addresses extra={str(extra_dict)}''')

    serializer = GetNearestAddressesSerializer( attrs=request_data, user=request.state.user, extra=extra_dict )
    data = await serializer.validate()

    response = codes[200].copy()
    response['message'] = f'Nearby address fetched successfully'
    response['details'] = data['details']
    log.info(f'''Request to list nearest address completed successfully extra={str(extra_dict)}''')
    return JSONResponse(content=response, status_code=200)

@router.put('/update')
async def update(request: Request, payload: UpdateAddressValidator, id: int = None):
    extra_dict = log_dict.copy()
    extra_dict['request_id'] = request.state.request_id
    extra_dict['endpoint'] = request.scope['path']

    request_data = await request.json()
    
    log.info(f'''Request received to update addresses extra={str(extra_dict)}''')

    if id is None:
        response = codes[400].copy()
        response['message'] = 'No address selected to update'
        log.error(f'Failed to update address because no id provided')
        raise HTTPException(status_code=400, detail=response)
    
    request_data['id'] = id

    serializer = UpdateAddressSerializer( attrs=request_data, user=request.state.user, extra=extra_dict )
    data = await serializer.validate()

    response = codes[201].copy()
    response['message'] = f'Address updated successfully'
    log.info(f'''Request to update address completed successfully extra={str(extra_dict)}''')
    return JSONResponse(content=response, status_code=201)

@router.delete('/delete')
async def delete(request: Request, id: int = None):
    extra_dict = log_dict.copy()
    extra_dict['request_id'] = request.state.request_id
    extra_dict['endpoint'] = request.scope['path']
    
    log.info(f'''Request received to delete addresses extra={str(extra_dict)}''')

    if id is None:
        response = codes[400].copy()
        response['message'] = 'No address selected to delete'
        log.error(f'Failed to delete address because no id provided')
        raise HTTPException(status_code=400, detail=response)
    
    request_data = {}
    request_data['id'] = id

    serializer = DeleteAddressSerializer( attrs=request_data, user=request.state.user, extra=extra_dict )
    data = await serializer.validate()

    response = codes[201].copy()
    response['message'] = f'Address deleted successfully'
    log.info(f'''Request to delete address completed successfully extra={str(extra_dict)}''')
    return JSONResponse(content=response, status_code=201)