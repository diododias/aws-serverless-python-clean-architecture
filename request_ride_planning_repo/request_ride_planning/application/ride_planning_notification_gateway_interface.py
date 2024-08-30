from abc import ABCMeta, abstractmethod

from request_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity


class RidePlanningNotificationGatewayInterface(metaclass=ABCMeta):
    @abstractmethod
    def notify_requested(self, ride_planning: RidePlanningEntity) -> str:
        raise NotImplementedError()

    @abstractmethod
    def notify_waiting_for_expiration(self, ride_planning: RidePlanningEntity) -> str:
        raise NotImplementedError()
