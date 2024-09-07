from aws_lambda_powertools.utilities.parser.models import SqsRecordModel
from aws_lambda_powertools.utilities.parser.types import Json


from pydantic import BaseModel


class ExpirationPayload(BaseModel):
    user_id: str
    ride_planning_id: str


class RidePlanningWaitingForExpirationEvent(BaseModel):
    data: ExpirationPayload
    name: str


class SqsWaitingForExpirationRecord(SqsRecordModel):
    body: Json[RidePlanningWaitingForExpirationEvent]
