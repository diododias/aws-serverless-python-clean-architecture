from datetime import datetime
from dataclasses import dataclass

from get_ride_planning.domain.entities.address_entity import AddressEntity
from get_ride_planning.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from get_ride_planning.domain.events.base_event import EventData, BaseEvent
from get_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from get_ride_planning.domain.value_objects.user_id import UserId


@dataclass
class RequestedPayload(EventData):
    user_id: UserId
    ride_planning_id: RidePlanningId
    address_from: AddressEntity
    address_to: AddressEntity
    departure_datetime: datetime
    status: RidePlanningStatusEnum
    created_at: datetime
    modified_at: datetime


@dataclass
class RidePlanningRequestedEvent(BaseEvent):
    data: RequestedPayload
    name = "RidePlanningRequestedEvent"
