from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import validator

from accounts.utils import email_is_valid
from accounts.utils import password_is_valid
from backend.status_codes import codes
from backend.log import log

class RegsterUserValidator(BaseModel):
    name: str
    email: str
    password: str

    @validator('name')
    def name_must_contain_space(cls, v):
        if len(v.split(' ')) < 2:
            response = codes[400].copy()
            response['message'] = 'Please provide full name'
            log.error(f'Failed to validate customuser data because full name missing.')
            raise HTTPException(status_code=400, detail=response)
        return v.title()

    @validator('email')
    def validate_email(cls, v):
        if not email_is_valid(v):
            response = codes[400].copy()
            response['message'] = 'Please provide a valid email'
            log.error(f'Failed to validate customuser data because invalid email.')
            raise HTTPException(status_code=400, detail=response)
        return v.title()
    
    @validator('password')
    def validate_password(cls, v):
        is_valid, message =  password_is_valid(v)

        if not is_valid:
            response = codes[400].copy()
            response['message'] = message
            log.error(f'Failed to validate customuser data {message}.')
            raise HTTPException(status_code=400, detail=response)
        return v.title()
    
class LoginUserValidator(BaseModel):
    email: str
    password: str

    @validator('email')
    def validate_email(cls, v):
        if not email_is_valid(v):
            response = codes[400].copy()
            response['message'] = 'Please provide a valid email'
            log.error(f'Failed to validate customuser data because invalid email.')
            raise HTTPException(status_code=400, detail=response)
        return v.title()