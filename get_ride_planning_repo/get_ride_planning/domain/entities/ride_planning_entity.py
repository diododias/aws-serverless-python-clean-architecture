from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC
from typing import List

from get_ride_planning.domain.entities.address_entity import AddressEntity
from get_ride_planning.domain.entities.ride_option_entity import RideOptionEntity
from get_ride_planning.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from get_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from get_ride_planning.domain.value_objects.user_id import UserId

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
    status: RidePlanningStatusEnum
    ride_options: List[RideOptionEntity] = field(default_factory=list)

    @property
    def is_time_expired(self) -> bool:
        expiration_time = self.created_at + timedelta(minutes=EXPIRATION_THRESHOLD_MINUTES)
        return expiration_time < datetime.now(UTC)

    def check_waiting_for_expiration(self) -> bool:
        if self.status in [RidePlanningStatusEnum.REQUESTED,
                           RidePlanningStatusEnum.WAITING_FOR_APPROVAL] and self.is_time_expired:
            self.status = RidePlanningStatusEnum.WAITING_FOR_EXPIRATION
            self.modified_at = datetime.now(UTC)
            return True
        return False
