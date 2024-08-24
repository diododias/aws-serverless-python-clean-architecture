from abc import ABCMeta, abstractmethod
from datetime import datetime

from request_ride_planning.domain.entities.address_entity import AddressEntity
from request_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from request_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from request_ride_planning.domain.value_objects.user_id import UserId


class RidePlanningPersistenceGatewayInterface(metaclass=ABCMeta):
    @abstractmethod
    def save(self, ride_planning: RidePlanningEntity) -> RidePlanningId:
        raise NotImplementedError()

    @abstractmethod
    def get_latest_by_user_id_ride_attributes(self,
                                              user_id: UserId,
                                              address_from: AddressEntity,
                                              address_to: AddressEntity,
                                              departure_datetime: datetime
                                              ) -> RidePlanningEntity | None:
        raise NotImplementedError()
