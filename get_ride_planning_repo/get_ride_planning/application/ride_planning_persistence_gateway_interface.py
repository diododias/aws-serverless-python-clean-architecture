from abc import ABCMeta, abstractmethod

from get_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from get_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from get_ride_planning.domain.value_objects.user_id import UserId


class RidePlanningPersistenceGatewayInterface(metaclass=ABCMeta):
    @abstractmethod
    def find_by_id_and_user_id(self, user_id: UserId, ride_planning_id: RidePlanningId) -> RidePlanningEntity | None:
        raise NotImplementedError()
