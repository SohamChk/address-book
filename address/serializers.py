import time
import math

from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound

from address.models import Address
from address.utils import get_coordinates
from backend.log import log
from backend.status_codes import codes

class AddAddressSerializer:

    def __init__(self, attrs={}, user=None, extra={}):
        self.attrs = attrs
        self.user = user
        self.extra = extra

    async def validate(self):
        attrs = self.attrs
        house_no = attrs.get('house_no', None)
        street = attrs.get('street', None)
        locality = attrs.get('locality', None)

        log.info(f'Serializer received request to add address with attrs={ attrs } extra={ str(self.extra) }')

        try:
            addr = f"{house_no}, {street}, {locality}"
            coord = await get_coordinates( addr=addr )
        except:
            coord = { 'lat': None, 'lng': None }
            log.warn(e)

        try:
            attrs['email'] = self.user
            attrs.update( coord )
            address = await Address.insert(extra=self.extra, **attrs)
            address.close()
        except Exception as e:
            response = codes[500].copy()
            response['message'] = 'Failed to add address'
            log.error(f'Failed to add address due to {str(e)}')
            raise HTTPException(status_code=500, detail=response)

        log.info(f'Serializer completed request to add address with attrs={ attrs } extra={ str(self.extra) }')
        return attrs
    
class ListAddressesSerializer:

    def __init__(self, attrs={}, user=None, extra={}):
        self.attrs = attrs
        self.user = user
        self.extra = extra

    async def validate(self):
        attrs = self.attrs

        log.info(f'Serializer received request to fetch address with attrs={ attrs } extra={ str(self.extra) }')

        try:
            attrs['email'] = self.user
            addresses = await Address.get(extra=self.extra, **attrs)
            attrs['details'] = [ entry[0].as_dict() for entry in addresses ]
        except NoResultFound as e:
            attrs['details'] = []
        except Exception as e:
            response = codes[500].copy()
            response['message'] = 'Failed to fetch address'
            log.error(f'Failed to fetch address due to {str(e)}')
            raise HTTPException(status_code=500, detail=response)
        
        log.info(f'Serializer completed request to fetch address with attrs={ attrs } extra={ str(self.extra) }')
        return attrs

class GetNearestAddressesSerializer:

    def __init__(self, attrs={}, user=None, extra={}):
        self.attrs = attrs
        self.user = user
        self.extra = extra

    async def validate(self):
        attrs = self.attrs
        house_no = attrs.pop('house_no', None)
        street = attrs.pop('street', None)
        locality = attrs.pop('locality', None)

        attrs['distance'] = ( 180 * attrs['distance'] )/( 6378100 * math.pi )

        log.info(f'Serializer received request to fetch nearest address with attrs={ attrs } extra={ str(self.extra) }')

        try:
            addr = f"{house_no}, {street}, {locality}"
            coord = await get_coordinates( addr=addr )
        except:
            coord = { 'lat': None, 'lng': None }
            log.warn(e)

        if coord.get('lat', None) is None or coord.get('lng', None) is None:
            response = codes[500].copy()
            response['message'] = 'Failed to fetch nearby address'
            log.error(f'Failed to fetch nearest address due to {str(e)}')
            raise HTTPException(status_code=500, detail=response)

        try:
            attrs['email'] = self.user
            attrs.update( coord )
            addresses = await Address.get_nearby_loc(extra=self.extra, **attrs)
            attrs['details'] = [ entry[0].as_dict() for entry in addresses ]
        except NoResultFound as e:
            attrs['details'] = []
        except Exception as e:
            response = codes[500].copy()
            response['message'] = 'Failed to fetch nearby address'
            log.error(f'Failed to fetch nearest address due to {str(e)}')
            raise HTTPException(status_code=500, detail=response)
        
        log.info(f'Serializer completed request to fetch nearest address with attrs={ attrs } extra={ str(self.extra) }')
        return attrs
    
class UpdateAddressSerializer:

    def __init__(self, attrs={}, user=None, extra={}):
        self.attrs = attrs
        self.user = user
        self.extra = extra

    async def validate(self):
        attrs = self.attrs

        log.info(f'Serializer received request to update address with attrs={ attrs } extra={ str(self.extra) }')

        try:
            conditions = {}
            conditions['email'] = self.user
            conditions['id'] = attrs.pop('id')
            if attrs:
                address = await Address.update(extra=self.extra, conditions=conditions, **attrs)
                address.close()
        except Exception as e:
            response = codes[500].copy()
            response['message'] = 'Failed to update address'
            log.error(f'Failed to update address due to {str(e)}')
            raise HTTPException(status_code=500, detail=response)

        log.info(f'Serializer completed request to update address with attrs={ attrs } extra={ str(self.extra) }')
        return attrs
    
class DeleteAddressSerializer:

    def __init__(self, attrs={}, user=None, extra={}):
        self.attrs = attrs
        self.user = user
        self.extra = extra

    async def validate(self):
        attrs = self.attrs

        log.info(f'Serializer received request to delete address with attrs={ attrs } extra={ str(self.extra) }')

        try:
            conditions = {}
            conditions['email'] = self.user
            conditions['id'] = attrs.pop('id')
            address = await Address.delete(extra=self.extra, conditions=conditions)
            address.close()
        except Exception as e:
            response = codes[500].copy()
            response['message'] = 'Failed to delete address'
            log.error(f'Failed to delete address due to {str(e)}')
            raise HTTPException(status_code=500, detail=response)

        log.info(f'Serializer completed request to delete address with attrs={ attrs } extra={ str(self.extra) }')
        return attrs