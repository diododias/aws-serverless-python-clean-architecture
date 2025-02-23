from datetime import datetime
from typing import Literal

from aws_lambda_powertools.utilities.parser.models import SnsNotificationModel
from aws_lambda_powertools.utilities.parser.types import Json

from pydantic import BaseModel


class RequestedEventSchema(BaseModel):
    user_id: str
    ride_planning_id: str


class MessageSchema(BaseModel):
    data: RequestedEventSchema
    name: str = Literal["RidePlanningRequestedEvent"]
    source: str
    spec_version: str
    data_content_type: str
    event_id: str
    correlation_id: str
    time: str


class SnsSchema(SnsNotificationModel):
    Message: Json[MessageSchema]
