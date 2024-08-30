from dataclasses import dataclass

from request_ride_planning.domain.events.base_event import EventData, BaseEvent
from request_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from request_ride_planning.domain.value_objects.user_id import UserId


@dataclass
class RequestedPayload(EventData):
    user_id: UserId
    ride_planning_id: RidePlanningId


@dataclass
class RidePlanningRequestedEvent(BaseEvent):
    data: RequestedPayload
    name = "RidePlanningRequestedEvent"
