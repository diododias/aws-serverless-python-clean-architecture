import json
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict

from request_ride_planning.domain.entities.address_entity import AddressEntity
from request_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from request_ride_planning.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from request_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from request_ride_planning.domain.value_objects.user_id import UserId
from request_ride_planning.drivers_adapters.dynamodb_constants import PRIMARY_KEY, SORT_KEY, TTL_IN_DAYS

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def map_ride_planning_to_persistence_schema(
        ride_planning: RidePlanningEntity,
        synthetic_id: str) -> Dict[str, str | Decimal | int]:
    ride_planning_item = dict()
    ride_planning_item[PRIMARY_KEY] = ride_planning.user_id
    ride_planning_item[SORT_KEY] = ride_planning.id
    ride_planning_item["ride_properties_hash"] = f"{synthetic_id}#CREATED_AT#{datetime.now().isoformat()}"
    ride_planning_item["address_from"] = json.dumps(ride_planning.address_from.__dict__)
    ride_planning_item["address_to"] = json.dumps(ride_planning.address_to.__dict__)
    ride_planning_item["status"] = ride_planning.status.value
    ride_planning_item["departure_datetime"] = ride_planning.departure_datetime.isoformat()
    ride_planning_item["created_at"] = ride_planning.created_at.strftime(DATETIME_FORMAT)
    ride_planning_item["modified_at"] = ride_planning.modified_at.strftime(DATETIME_FORMAT)
    ride_planning_item["time_to_live"] = Decimal((datetime.now() + timedelta(days=TTL_IN_DAYS)).timestamp())
    return ride_planning_item


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
        departure_datetime=datetime.fromisoformat(ride_planning_dto.get("departure_datetime")),
        created_at=datetime.fromisoformat(ride_planning_dto.get("created_at")),
        modified_at=datetime.fromisoformat(ride_planning_dto.get("modified_at")),
        status=RidePlanningStatusEnum[ride_planning_dto.get("status")]
    )
