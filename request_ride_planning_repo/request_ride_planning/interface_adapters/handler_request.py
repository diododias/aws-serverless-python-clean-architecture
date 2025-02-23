import datetime
from typing import TypedDict

from pydantic import BaseModel, Field, Json


class AddressRequest(BaseModel):
    street: str = Field(max_length=70)
    city: str = Field(max_length=70)
    country: str = Field(max_length=70)
    postal_code: str = Field(max_length=70)


class RequestBody(BaseModel):
    address_from: AddressRequest
    address_to: AddressRequest
    departure_datetime: datetime.datetime


class RequestContextIdentity(BaseModel):
    user: int


class RequestContext(BaseModel):
    identity: RequestContextIdentity


class HandlerRequest(TypedDict):
    body: str | RequestBody  # json string
    requestContext: RequestContext
