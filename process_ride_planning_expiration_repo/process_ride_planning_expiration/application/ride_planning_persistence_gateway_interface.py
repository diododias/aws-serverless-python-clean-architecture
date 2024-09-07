from abc import ABCMeta, abstractmethod

from process_ride_planning_expiration.domain.entities.ride_planning_entity import RidePlanningEntity
from process_ride_planning_expiration.domain.value_objects.ride_planning_id import RidePlanningId
from process_ride_planning_expiration.domain.value_objects.user_id import UserId


class RidePlanningPersistenceGatewayInterface(metaclass=ABCMeta):
    @abstractmethod
    def find_by_id_and_user_id(self, user_id: UserId, ride_planning_id: RidePlanningId) -> RidePlanningEntity | None:
        raise NotImplementedError()

    @abstractmethod
    def update(self, ride_planning: RidePlanningEntity) -> None:
        raise NotImplementedError()
