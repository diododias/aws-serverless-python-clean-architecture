import hashlib

from datetime import datetime
from typing import NewType
from boto3.dynamodb.conditions import Key
from aws_lambda_powertools import Logger

from request_ride_planning.application.ride_planning_persistence_gateway_interface import (
    RidePlanningPersistenceGatewayInterface)
from request_ride_planning.domain.entities.address_entity import AddressEntity
from request_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from request_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from request_ride_planning.domain.value_objects.user_id import UserId
from request_ride_planning.drivers_adapters.dynamodb_constants import RIDE_PROPERTIES_HASH, PRIMARY_KEY, SORT_KEY
from request_ride_planning.drivers_adapters.ride_planning_dynamodb_mapper import (
    map_ride_planning_to_persistence_schema,
    map_persistence_schema_to_ride_planning)

DynamodbResourceTable = NewType("DynamodbResourceTable", object)


class RidePlanningDynamodbGateway(RidePlanningPersistenceGatewayInterface):
    _dynamodb_resource_table: DynamodbResourceTable
    _logger = Logger(child=True)

    def __init__(self, dynamodb_resource_table: DynamodbResourceTable):
        self._dynamodb_resource_table = dynamodb_resource_table

    @staticmethod
    def _generate_synthetic_id(address_from: AddressEntity,
                               address_to: AddressEntity,
                               departure_datetime: datetime
                               ) -> str:
        """
        Generates a hash of the attributes of a ride planning to be used as a Secondary ID.
        This practice is useful to help dynamodb find ride plannings that have the same attributes.

        Args:
            address_from: start point of a ride
            address_to: end point of a ride
            departure_datetime: date and time to start a ride

        Returns: Synthetic ID / Secondary ID
        """
        data = str(address_from.__dict__) + str(address_to.__dict__) + departure_datetime.isoformat()
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def save(self, ride_planning: RidePlanningEntity) -> RidePlanningId:
        """
        Put ride planning in the persistence layer

        Args:
            ride_planning:

        Returns: RidePlanningId
        """
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
        """
        Get latest Ride Planning that have same ride attributes

        Args:
            user_id: User ID
            address_from: start point of a ride
            address_to: end point of a ride
            departure_datetime: date and time to start a ride

        Returns: RidePlanning Object if is found
        """
        synthetic_id: str = self._generate_synthetic_id(address_from, address_to, departure_datetime)
        self._logger.debug("Looking for a ride planning with same attributes")
        response = self._dynamodb_resource_table.query(
            IndexName=RIDE_PROPERTIES_HASH,
            KeyConditionExpression=Key(PRIMARY_KEY).eq(user_id) & Key(RIDE_PROPERTIES_HASH).begins_with(synthetic_id),
            ConsistentRead=True,
            Limit=1,
            ScanIndexForward=False
        )
        if response.get("Items"):
            item = response.get("Items")[0]
            self._logger.debug("get ride planning item")
            ride_response = self._dynamodb_resource_table.get_item(
                Key={
                    str(PRIMARY_KEY): item.get(PRIMARY_KEY),
                    str(SORT_KEY): item.get(SORT_KEY)
                }
            )
            if "Item" in ride_response:
                ride = ride_response.get("Item")
                self._logger.debug("map item to ride planning entity")
                return map_persistence_schema_to_ride_planning(ride)
        return None
