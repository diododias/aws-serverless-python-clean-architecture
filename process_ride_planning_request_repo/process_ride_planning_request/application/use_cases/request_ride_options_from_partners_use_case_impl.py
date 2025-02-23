from typing import List, Optional

from process_ride_planning_request.application.gateways.ride_option_partner_gateway_interface import \
    RideOptionPartnerGatewayInterface
from process_ride_planning_request.domain.entities.ride_planning_entity import RidePlanningEntity
from process_ride_planning_request.domain.entities.ride_option_entity import RideOptionEntity
from process_ride_planning_request.domain.use_cases.request_ride_options_from_partners_use_case_interface import \
    RequestRideOptionsFromPartnersUseCaseInterface


class RequestRideOptionsFromPartnersUseCaseImpl(RequestRideOptionsFromPartnersUseCaseInterface):
    _partners_gateways: List[RideOptionPartnerGatewayInterface]

    def __init__(self, partners_gateways: List[RideOptionPartnerGatewayInterface]):
        self._partners_gateways = partners_gateways

    def execute(self, ride_planning: RidePlanningEntity) -> None:
        for partner_gateway in self._partners_gateways:
            ride_option: Optional[RideOptionEntity] = partner_gateway.request_ride_option(ride_planning)
            if ride_option:
                ride_planning.add_ride_option(ride_option)
