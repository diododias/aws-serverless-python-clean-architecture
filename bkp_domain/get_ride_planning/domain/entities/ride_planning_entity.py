from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC
from typing import List

from get_ride_planning.domain.entities.address_entity import AddressEntity
from get_ride_planning.domain.entities.ride_option_entity import RideOptionEntity
from get_ride_planning.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from get_ride_planning.domain.exceptions.invalid_state import InvalidState
from get_ride_planning.domain.exceptions.ride_option_not_found import RideOptionNotFound
from get_ride_planning.domain.value_objects.ride_option_id import RideOptionId
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
        return (self.created_at + timedelta(minutes=EXPIRATION_THRESHOLD_MINUTES)) < datetime.now(UTC)

    @property
    def is_completed(self) -> bool:
        return (self.status in [RidePlanningStatusEnum.EXPIRED,
                                RidePlanningStatusEnum.APPROVED,
                                RidePlanningStatusEnum.REQUEST_FAILED]
                or self.is_time_expired)

    def check_waiting_for_expiration(self) -> bool:
        if (self.status in [RidePlanningStatusEnum.REQUESTED,
                            RidePlanningStatusEnum.WAITING_FOR_APPROVAL]
                and self.is_time_expired):
            self.status = RidePlanningStatusEnum.WAITING_FOR_EXPIRATION
            self.modified_at = datetime.now(UTC)
            return True
        return False

    def set_status_to_expired(self) -> None:
        if self.check_waiting_for_expiration():
            self.status = RidePlanningStatusEnum.EXPIRED
            self.modified_at = datetime.now(UTC)

    def set_ride_options(self, ride_options: List[RideOptionEntity]) -> None:
        if not RidePlanningStatusEnum.REQUESTED:
            raise InvalidState("to set ride options the status must be REQUESTED")
        self.ride_options = ride_options
        self.status = RidePlanningStatusEnum.WAITING_FOR_APPROVAL
        self.modified_at = datetime.now(UTC)

    def approve_ride_option(self, ride_option_id: RideOptionId) -> None:
        if not RidePlanningStatusEnum.WAITING_FOR_APPROVAL:
            raise InvalidState("To approve a ride the status must be WAITING FOR APPROVAL")
        # Iterate over ride options to find the correct ride option
        for i, ride_opt in enumerate(self.ride_options):
            if ride_opt.id == ride_option_id:
                ride_opt.accepted = True
                self.ride_options[i] = ride_opt
                self.status = RidePlanningStatusEnum.APPROVED
                self.modified_at = datetime.now(UTC)
                return
        raise RideOptionNotFound(ride_option_id)
