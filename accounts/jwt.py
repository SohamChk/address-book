from datetime import datetime
from datetime import timedelta
from typing import Optional

from jose import jwt

from backend.config import get_settings

def get_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta( minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES )

    to_encode.update({"exp": expire, 'iat': datetime.utcnow()})
    encoded_jwt = jwt.encode( to_encode, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM )

    return encoded_jwt