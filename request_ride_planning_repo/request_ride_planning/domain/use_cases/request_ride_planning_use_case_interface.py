from abc import ABCMeta, abstractmethod
from datetime import datetime

from request_ride_planning.domain.entities.address_entity import AddressEntity
from request_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from request_ride_planning.domain.value_objects.user_id import UserId


class RequestRidePlanningUseCaseInterface(metaclass=ABCMeta):
    @abstractmethod
    def execute(self,
                user_id: UserId,
                address_from: AddressEntity,
                address_to: AddressEntity,
                departure_datetime: datetime) -> RidePlanningId:
        raise NotImplementedError()
