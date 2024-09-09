import json
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict

from process_ride_planning_expiration.domain.entities.address_entity import AddressEntity
from process_ride_planning_expiration.domain.entities.ride_option_entity import RideOptionEntity
from process_ride_planning_expiration.domain.entities.ride_planning_entity import RidePlanningEntity
from process_ride_planning_expiration.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from process_ride_planning_expiration.domain.value_objects.ride_planning_id import RidePlanningId
from process_ride_planning_expiration.domain.value_objects.user_id import UserId
from process_ride_planning_expiration.drivers_adapters.dynamodb_constants import PRIMARY_KEY, SORT_KEY


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def map_persistence_schema_to_ride_planning(ride_planning_dto: Dict[str, str | Decimal | int]) -> RidePlanningEntity:
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
        status=RidePlanningStatusEnum[ride_planning_dto.get("ride_status")]
    )
