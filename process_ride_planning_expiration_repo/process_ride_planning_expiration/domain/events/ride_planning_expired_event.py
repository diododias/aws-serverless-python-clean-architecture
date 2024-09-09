from dataclasses import dataclass

from process_ride_planning_expiration.domain.events.base_event import BaseEvent, EventData
from process_ride_planning_expiration.domain.value_objects.ride_planning_id import RidePlanningId
from process_ride_planning_expiration.domain.value_objects.user_id import UserId


@dataclass
class ExpirationPayload(EventData):
    user_id: UserId
    ride_planning_id: RidePlanningId


@dataclass
class RidePlanningExpiredEvent(BaseEvent):
    data: ExpirationPayload
    name: str = "RidePlanningExpiredEvent"
