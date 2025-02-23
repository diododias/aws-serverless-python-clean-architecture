from dataclasses import dataclass

from process_ride_planning_request.domain.events.base_event import BaseEvent, EventData
from process_ride_planning_request.domain.value_objects.ride_planning_id import RidePlanningId
from process_ride_planning_request.domain.value_objects.user_id import UserId


@dataclass
class WaitingForApproveData(EventData):
    user_id: UserId
    ride_planning_id: RidePlanningId


@dataclass
class RidePlanningWaitingForApproveEvent(BaseEvent):
    data: WaitingForApproveData
    name: str = "RidePlanningWaitingForApproveEvent"
