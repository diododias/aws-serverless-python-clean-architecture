from dataclasses import dataclass
from decimal import Decimal

from get_ride_planning.domain.entities.ride_provider_enum import RideProviderEnum
from get_ride_planning.domain.entities.ride_tier_enum import RideTierEnum
from get_ride_planning.domain.value_objects.ride_option_id import RideOptionId


@dataclass
class RideOption:
    id: RideOptionId
    provider_id: str
    provider: RideProviderEnum
    tier: RideTierEnum
    price: Decimal
    accepted: bool = False
