import json
from datetime import datetime
from decimal import Decimal
from typing import Dict

from get_ride_planning.domain.entities.address_entity import AddressEntity
from get_ride_planning.domain.entities.ride_option_entity import RideOptionEntity
from get_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from get_ride_planning.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from get_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from get_ride_planning.domain.value_objects.user_id import UserId
from get_ride_planning.drivers_adapters.dynamodb_constants import SORT_KEY, PRIMARY_KEY


def map_persistence_schema_to_ride_planning(ride_planning_dto: Dict[str, str | Decimal | int]) -> RidePlanningEntity:
    print(ride_planning_dto)
    address_from_dto = json.loads(ride_planning_dto.get("address_from"))
    address_to_dto = json.loads(ride_planning_dto.get("address_from"))
    return RidePlanningEntity(
        id=RidePlanningId(ride_planning_dto.get(SORT_KEY)),
        user_id=UserId(ride_planning_dto.get(PRIMARY_KEY)),
        address_from=AddressEntity(
            address_from_dto.get("street"),
            address_from_dto.get("city"),
            address_from_dto.get("country"),
            address_from_dto.get("postal_code")
        ),
        address_to=AddressEntity(
            address_to_dto.get("street"),
            address_to_dto.get("city"),
            address_to_dto.get("country"),
            address_to_dto.get("postal_code")
        ),
        ride_options=[RideOptionEntity(**json.loads(ro)) for ro in ride_planning_dto.get("ride_options")],
        departure_datetime=datetime.fromisoformat(ride_planning_dto.get("departure_datetime")),
        created_at=datetime.fromisoformat(ride_planning_dto.get("created_at")),
        modified_at=datetime.fromisoformat(ride_planning_dto.get("modified_at")),
        status=RidePlanningStatusEnum[ride_planning_dto.get("status")]
    )
