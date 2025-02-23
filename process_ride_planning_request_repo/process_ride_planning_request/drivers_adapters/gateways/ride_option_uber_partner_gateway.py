import uuid
from decimal import Decimal
import random
from typing import Optional

from process_ride_planning_request.application.gateways.ride_option_partner_gateway_interface import \
    RideOptionPartnerGatewayInterface
from process_ride_planning_request.domain.entities.ride_option_entity import RideOptionEntity
from process_ride_planning_request.domain.entities.ride_planning_entity import RidePlanningEntity
from process_ride_planning_request.domain.entities.ride_provider_enum import RideProviderEnum
from process_ride_planning_request.domain.entities.ride_tier_enum import RideTierEnum
from process_ride_planning_request.domain.value_objects.ride_option_id import RideOptionId


class RideOptionUberPartnerGateway(RideOptionPartnerGatewayInterface):
    def request_ride_option(self, ride_planning: RidePlanningEntity) -> Optional[RideOptionEntity]:
        #  Simulate call to external API and return an Ride Option
        return RideOptionEntity(
            id=RideOptionId(uuid.uuid4().hex),
            provider_id="33",
            provider=RideProviderEnum.UBER,
            tier=RideTierEnum.BASIC,
            price=Decimal(random.uniform(4.5, 14.28)),
            accepted=False
        )
