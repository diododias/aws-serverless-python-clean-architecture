from dataclasses import dataclass

from get_ride_planning.domain.events.base_event import BaseEvent, EventData
from get_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from get_ride_planning.domain.value_objects.user_id import UserId


@dataclass
class ExpirationData(EventData):
    user_id: UserId
    ride_planning_id: RidePlanningId


@dataclass
class RidePlanningWaitingForExpirationEvent(BaseEvent):
    data: ExpirationData
    name: str = "RidePlanningWaitingForExpirationEvent"
