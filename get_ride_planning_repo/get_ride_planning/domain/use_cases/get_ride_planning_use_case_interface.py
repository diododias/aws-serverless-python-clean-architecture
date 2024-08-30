from abc import ABCMeta, abstractmethod

from get_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from get_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from get_ride_planning.domain.value_objects.user_id import UserId


class GetRidePlanningUseCaseInterface(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, user_id: UserId, ride_planning_id: RidePlanningId) -> RidePlanningEntity:
        raise NotImplementedError()
