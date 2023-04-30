import time

from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound

from accounts.models import Users
from accounts.jwt import get_access_token
from backend.config import get_settings
from backend.db.hash import Hasher
from backend.log import log
from backend.status_codes import codes

class RegisterUserSerializer:

    def __init__(self, attrs={}, user=None, extra={}):
        self.attrs = attrs
        self.user = user
        self.extra = extra

    async def validate(self):
        attrs = self.attrs

        log.info(f'Serializer received request to register user with attrs={ attrs } extra={ str(self.extra) }')

        attrs['password'] = Hasher.get_password_hash(attrs['password'])

        try:
            user = await Users.insert(extra=self.extra, **attrs)
            user.close()
        except Exception as e:
            response = codes[500].copy()
            response['message'] = 'Failed to register user'
            log.error(f'Failed to register user due to {str(e)}')
            raise HTTPException(status_code=500, detail=response)

        log.info(f'Serializer completed request to register user with attrs={ attrs } extra={ str(self.extra) }')
        return attrs
    
class LoginUserSerializer:

    def __init__(self, attrs={}, user=None, extra={}):
        self.attrs = attrs
        self.user = user
        self.extra = extra

    async def validate(self):
        attrs = self.attrs

        log.info(f'Serializer received request to login user with attrs={ attrs } extra={ str(self.extra) }')

        password = attrs.pop('password')

        try:
            user = await Users.get(extra=self.extra, **attrs)
        except NoResultFound as e:
            response = codes[404].copy()
            response['message'] = 'No such user found'
            log.error(f'Failed to login user due to {str(e)}')
            raise HTTPException(status_code=404, detail=response)
        except Exception as e:
            response = codes[500].copy()
            response['message'] = 'Failed to login user'
            log.error(f'Failed to login user due to {str(e)}')
            raise HTTPException(status_code=500, detail=response)
        
        userdetail = user[0][0].as_dict()

        if not Hasher.verify_password(password, userdetail['password']):
            response = codes[401].copy()
            response['message'] = 'Incorrect password provided'
            raise HTTPException(status_code=401, detail=response)
        
        access_token = get_access_token( { 'email': self.attrs['email'] } )
        
        attrs['details'] = { 'access_token': access_token, 'expires_in': get_settings().ACCESS_TOKEN_EXPIRE_MINUTES * 60, 'expires_at': int(time.time()) + int(get_settings().ACCESS_TOKEN_EXPIRE_MINUTES * 60), 'token_type': 'bearer' }

        log.info(f'Serializer completed request to login user with attrs={ attrs } extra={ str(self.extra) }')
        return attrs