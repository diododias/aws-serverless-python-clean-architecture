from abc import ABCMeta, abstractmethod
from typing import Optional

from process_ride_planning_request.domain.entities.ride_option_entity import RideOptionEntity
from process_ride_planning_request.domain.entities.ride_planning_entity import RidePlanningEntity


class RideOptionPartnerGatewayInterface(metaclass=ABCMeta):
    @abstractmethod
    def request_ride_option(self, ride_planning: RidePlanningEntity) -> Optional[RideOptionEntity]:
        raise NotImplementedError()
