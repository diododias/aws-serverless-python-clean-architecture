from abc import ABCMeta, abstractmethod

from src.domain.entities.ride_planning_entity import RidePlanningEntity


class RidePlanningNotificationGateway(metaclass=ABCMeta):
    @abstractmethod
    def send(self, ride_planning: RidePlanningEntity) -> str:
        raise NotImplementedError()
