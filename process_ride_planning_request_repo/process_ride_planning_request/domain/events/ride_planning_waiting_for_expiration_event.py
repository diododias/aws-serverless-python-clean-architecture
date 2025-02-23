from dataclasses import dataclass

from process_ride_planning_request.domain.events.base_event import EventData, BaseEvent
from process_ride_planning_request.domain.value_objects.ride_planning_id import RidePlanningId
from process_ride_planning_request.domain.value_objects.user_id import UserId


@dataclass
class ExpirationData(EventData):
    user_id: UserId
    ride_planning_id: RidePlanningId


@dataclass
class RidePlanningWaitingForExpirationEvent(BaseEvent):
    data: ExpirationData
    name: str = "RidePlanningWaitingForExpirationEvent"
