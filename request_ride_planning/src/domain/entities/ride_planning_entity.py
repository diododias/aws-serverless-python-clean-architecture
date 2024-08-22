from dataclasses import dataclass
from datetime import datetime, timedelta, UTC

from src.domain.entities.address_entity import AddressEntity
from src.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from src.domain.value_objects.ride_planning_id import RidePlanningId
from src.domain.value_objects.user_id import UserId

# TODO: VARIAVEL DE AMBIENTE
EXPIRATION_THRESHOLD_MINUTES = 5


@dataclass
class RidePlanningEntity:
    id: RidePlanningId
    user_id: UserId
    address_from: AddressEntity
    address_to: AddressEntity
    departure_datetime: datetime
    created_at: datetime
    modified_at: datetime
    status: RidePlanningStatusEnum = RidePlanningStatusEnum.REQUESTED

    def is_done(self) -> bool:
        is_time_expired = (self.created_at + timedelta(minutes=EXPIRATION_THRESHOLD_MINUTES)) < datetime.now(UTC)
        return (self.status == RidePlanningStatusEnum.EXPIRED or
                self.status == RidePlanningStatusEnum.APPROVED or
                is_time_expired)
