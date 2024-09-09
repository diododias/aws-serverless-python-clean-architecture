from datetime import datetime

from aws_lambda_powertools.utilities.parser.models import SnsNotificationModel, SqsRecordModel
from aws_lambda_powertools.utilities.parser.types import Json


from pydantic import BaseModel


class ExpirationPayload(BaseModel):
    user_id: str
    ride_planning_id: str


class RidePlanningWaitingForExpirationEvent(BaseModel):
    data: ExpirationPayload
    name: str
    source: str
    spec_version: str
    data_content_type: str
    event_id: str
    time: datetime


class SnsWaitingForExpirationMessage(SnsNotificationModel):
    Message: Json[RidePlanningWaitingForExpirationEvent]

