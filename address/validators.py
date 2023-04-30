from pydantic import BaseModel
from typing import Optional

class AddAddressValidator(BaseModel):
    house_no: str
    street: str
    locality: str
    city: str
    state: str
    postal_code: str
    country: str

class UpdateAddressValidator(BaseModel):
    house_no: Optional[str]
    street: Optional[str]
    locality: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]

class NearbyAddressValidator(BaseModel):
    house_no: str
    street: str
    locality: str