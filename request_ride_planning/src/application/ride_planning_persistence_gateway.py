from abc import ABCMeta, abstractmethod
from datetime import datetime

from src.domain.entities.address_entity import AddressEntity
from src.domain.entities.ride_planning_entity import RidePlanningEntity
from src.domain.value_objects.ride_planning_Id import RidePlanningId
from src.domain.value_objects.user_id import UserId


class RidePlanningPersistenceGateway(metaclass=ABCMeta):
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
