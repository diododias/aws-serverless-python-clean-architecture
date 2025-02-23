from abc import ABCMeta, abstractmethod

from process_ride_planning_request.domain.entities.ride_planning_entity import RidePlanningEntity


class RequestRideOptionsFromPartnersUseCaseInterface(metaclass=ABCMeta):

    @abstractmethod
    def execute(self, ride_planning: RidePlanningEntity) -> None:
        raise NotImplementedError()
