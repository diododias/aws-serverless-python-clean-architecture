import datetime
from typing import TypedDict

from pydantic import BaseModel, Field


class BodyRequest(BaseModel):
    ride_planning_id: str = Field(max_length=41)
    user_id: str = Field(max_length=41)


class HandlerRequest(TypedDict):
    body: BodyRequest
