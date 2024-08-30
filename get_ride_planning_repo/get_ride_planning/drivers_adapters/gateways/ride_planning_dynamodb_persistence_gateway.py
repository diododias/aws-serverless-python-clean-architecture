from typing import NewType
from aws_lambda_powertools import Logger

from get_ride_planning.application.ride_planning_persistence_gateway_interface import \
    RidePlanningPersistenceGatewayInterface
from get_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from get_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from get_ride_planning.domain.value_objects.user_id import UserId
from get_ride_planning.drivers_adapters.dynamodb_constants import PRIMARY_KEY, SORT_KEY
from get_ride_planning.drivers_adapters.ride_planning_dynamodb_mapper import map_persistence_schema_to_ride_planning

DynamodbResourceTable = NewType("DynamodbResourceTable", object)


class RidePlanningDynamodbGateway(RidePlanningPersistenceGatewayInterface):
    _dynamodb_resource_table: DynamodbResourceTable
    _logger = Logger(child=True)

    def __init__(self, dynamodb_resource_table: DynamodbResourceTable):
        self._dynamodb_resource_table = dynamodb_resource_table

    def find_by_id_and_user_id(self, ride_planning_id: RidePlanningId, user_id: UserId) -> RidePlanningEntity | None:
        item = self._dynamodb_resource_table.get_item(
            Key={
                str(PRIMARY_KEY): user_id,
                str(SORT_KEY): ride_planning_id
            }
        )
        if "Item" in item:
            ride = item.get("Item")
            self._logger.debug("map item to ride planning entity")
            return map_persistence_schema_to_ride_planning(ride)
