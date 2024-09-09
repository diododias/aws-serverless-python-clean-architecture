from typing import NewType
from aws_lambda_powertools import Logger

from process_ride_planning_expiration.application.ride_planning_persistence_gateway_interface import (
    RidePlanningPersistenceGatewayInterface)
from process_ride_planning_expiration.domain.entities.ride_planning_entity import RidePlanningEntity
from process_ride_planning_expiration.domain.value_objects.ride_planning_id import RidePlanningId
from process_ride_planning_expiration.domain.value_objects.user_id import UserId
from process_ride_planning_expiration.drivers_adapters.dynamodb_constants import PRIMARY_KEY, SORT_KEY
from process_ride_planning_expiration.drivers_adapters.mappers.ride_planning_dynamodb_mapper import (
    map_persistence_schema_to_ride_planning)

DynamodbResourceTable = NewType("DynamodbResourceTable", object)


class RidePlanningDynamodbPersistenceGateway(RidePlanningPersistenceGatewayInterface):
    _dynamodb_resource_table: DynamodbResourceTable
    _logger = Logger(child=True)

    def __init__(self, dynamodb_resource_table: DynamodbResourceTable):
        self._dynamodb_resource_table = dynamodb_resource_table

    def update(self, ride_planning: RidePlanningEntity) -> RidePlanningId:
        self._logger.debug(f"Update Item: {ride_planning}")
        self._dynamodb_resource_table.update_item(
            Key={
                str(PRIMARY_KEY): ride_planning.user_id,
                str(SORT_KEY): ride_planning.id
            },
            UpdateExpression="set ride_status = :s, modified_at = :m",
            ExpressionAttributeValues={
                ":s": ride_planning.status.value,
                ":m": ride_planning.modified_at.isoformat()
            }
        )
        return ride_planning.id

    def find_by_id_and_user_id(self, user_id: UserId, ride_planning_id: RidePlanningId) -> RidePlanningEntity | None:
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
