from datetime import datetime
import hashlib
from typing import Any

from boto3.dynamodb.conditions import Key

from src.application.ride_planning_persistence_gateway import RidePlanningPersistenceGateway
from src.domain.entities.address_entity import AddressEntity
from src.domain.entities.ride_planning_entity import RidePlanningEntity
from src.domain.value_objects.user_id import UserId
from src.drivers_adapters.constants import UNIQUE_RIDE_PROPERTIES_INDEX, PRIMARY_KEY, SORT_KEY
from src.drivers_adapters.ride_planning_mapper import map_ride_planning_to_persistence_schema, \
    map_persistence_schema_to_ride_planning


class RidePlanningPersistenceGatewayImpl(RidePlanningPersistenceGateway):
    # TODO: encontrar um tipo compativel
    _dynamodb_resource_table: Any

    def __init__(self, dynamodb_resource_table: object):
        self._dynamodb_resource_table = dynamodb_resource_table

    @staticmethod
    def _generate_synthetic_id(address_from: AddressEntity,
                               address_to: AddressEntity,
                               departure_datetime: datetime
                               ) -> str:
        data = str(address_from.__dict__) + str(address_to.__dict__) + departure_datetime.isoformat()
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def save(self, ride_planning: RidePlanningEntity) -> str:
        synthetic_id: str = self._generate_synthetic_id(
            ride_planning.address_from,
            ride_planning.address_to,
            ride_planning.departure_datetime
        )
        ride_planning_item = map_ride_planning_to_persistence_schema(ride_planning, synthetic_id)
        self._dynamodb_resource_table.put_item(Item=ride_planning_item)
        return ride_planning.id

    def get_latest_by_user_id_ride_attributes(self,
                                                    user_id: UserId,
                                                    address_from: AddressEntity,
                                                    address_to: AddressEntity,
                                                    departure_datetime: datetime
                                                    ) -> RidePlanningEntity | None:
        synthetic_id: str = self._generate_synthetic_id(address_from, address_to, departure_datetime)
        response = self._dynamodb_resource_table.query(
            IndexName=UNIQUE_RIDE_PROPERTIES_INDEX,
            KeyConditionExpression=Key(PRIMARY_KEY).eq(user_id) & Key("ride_properties_hash").begins_with(synthetic_id),
            ConsistentRead=True,
            Limit=1,
            ScanIndexForward=False
        )
        if response.get("Items"):
            item = response.get("Items")[0]
            ride_response = self._dynamodb_resource_table.get_item(
                Key={
                    str(PRIMARY_KEY): item.get(PRIMARY_KEY),
                    str(SORT_KEY): item.get(SORT_KEY)
                }
            )
            if "Item" in ride_response:
                ride = ride_response.get("Item")
                return map_persistence_schema_to_ride_planning(ride)
        return None
