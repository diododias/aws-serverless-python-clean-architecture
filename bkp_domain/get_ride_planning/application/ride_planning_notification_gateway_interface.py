from abc import ABCMeta, abstractmethod

from get_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity


class RidePlanningNotificationGatewayInterface(metaclass=ABCMeta):

    @abstractmethod
    def notify_waiting_for_expiration(self, ride_planning: RidePlanningEntity):
        raise NotImplementedError()
