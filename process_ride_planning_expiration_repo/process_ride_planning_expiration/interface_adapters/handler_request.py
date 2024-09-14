from datetime import datetime

from aws_lambda_powertools.utilities.parser.models import SnsNotificationModel
from aws_lambda_powertools.utilities.parser.types import Json

from pydantic import BaseModel


class WaitingForExpirationEventSchema(BaseModel):
    user_id: str
    ride_planning_id: str


class MessageSchema(BaseModel):
    data: WaitingForExpirationEventSchema
    name: str
    source: str
    spec_version: str
    data_content_type: str
    event_id: str
    correlation_id: str
    time: str


class SnsSchema(SnsNotificationModel):
    Message: Json[MessageSchema]
