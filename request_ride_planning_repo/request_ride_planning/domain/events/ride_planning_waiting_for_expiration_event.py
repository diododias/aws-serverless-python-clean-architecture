from dataclasses import dataclass

from request_ride_planning.domain.events.base_event import BaseEvent, EventData
from request_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from request_ride_planning.domain.value_objects.user_id import UserId


@dataclass
class ExpirationPayload(EventData):
    user_id: UserId
    ride_planning_id: RidePlanningId


@dataclass
class RidePlanningWaitingForExpirationEvent(BaseEvent):
    data: ExpirationPayload
    name = "RidePlanningWaitingForExpirationEvent"
