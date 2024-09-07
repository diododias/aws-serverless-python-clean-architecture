from dataclasses import dataclass
from decimal import Decimal

from process_ride_planning_expiration.domain.entities.ride_provider_enum import RideProviderEnum
from process_ride_planning_expiration.domain.entities.ride_tier_enum import RideTierEnum
from process_ride_planning_expiration.domain.value_objects.ride_option_id import RideOptionId


@dataclass
class RideOptionEntity:
    id: RideOptionId
    provider_id: str
    provider: RideProviderEnum
    tier: RideTierEnum
    price: Decimal
    accepted: bool = False
