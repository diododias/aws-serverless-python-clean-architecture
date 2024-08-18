import datetime
from typing import TypedDict

from pydantic import BaseModel, Field

# TODO: importar qndo corrigirem o bug
# from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventV2Model


class AddressRequest(BaseModel):
    street: str = Field(max_length=70)
    city: str = Field(max_length=70)
    country: str = Field(max_length=70)
    postal_code: str = Field(max_length=70)


class BodyRequest(BaseModel):
    address_from: AddressRequest
    address_to: AddressRequest
    departure_datetime: datetime.datetime
    user_id: str = Field(max_length=70)


class HandlerRequest(TypedDict):
    body: BodyRequest
