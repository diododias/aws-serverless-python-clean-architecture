from abc import ABCMeta, abstractmethod

from request_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity


class RidePlanningNotificationGatewayInterface(metaclass=ABCMeta):
    @abstractmethod
    def send(self, ride_planning: RidePlanningEntity) -> str:
        raise NotImplementedError()
