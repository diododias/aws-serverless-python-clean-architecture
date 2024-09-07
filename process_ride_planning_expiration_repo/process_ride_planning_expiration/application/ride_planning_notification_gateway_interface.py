from abc import ABCMeta, abstractmethod

from process_ride_planning_expiration.domain.entities.ride_planning_entity import RidePlanningEntity


class RidePlanningNotificationGatewayInterface(metaclass=ABCMeta):

    @abstractmethod
    def notify_expired(self, ride_planning: RidePlanningEntity):
        raise NotImplementedError()
