import dataclasses

from typing import NewType, Dict, Optional
from aws_lambda_powertools import Logger

from process_ride_planning_expiration.application.persistence_gateway_interface import (
    PersistenceGatewayInterface)
from process_ride_planning_expiration.domain.entities.ride_planning_entity import RidePlanningEntity
from process_ride_planning_expiration.domain.value_objects.ride_planning_id import RidePlanningId
from process_ride_planning_expiration.domain.value_objects.user_id import UserId
from process_ride_planning_expiration.drivers_adapters.dynamodb_constants import PRIMARY_KEY, SORT_KEY
from process_ride_planning_expiration.drivers_adapters.mappers.ride_planning_dynamodb_mapper import (
    map_persistence_schema_to_ride_planning)

DynamodbResourceTable = NewType("DynamodbResourceTable", object)


class DynamodbPersistenceGateway(PersistenceGatewayInterface):
    _dynamodb_resource_table: DynamodbResourceTable
    _logger = Logger(child=True)

    def __init__(self, dynamodb_resource_table: DynamodbResourceTable):
        self._dynamodb_resource_table = dynamodb_resource_table

    def update(self, ride_planning: RidePlanningEntity) -> RidePlanningId:
        self._logger.debug(f"Update Item: {dataclasses.asdict(ride_planning)}")
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
        self._logger.info(f"ride_planning_id {ride_planning.id} was persisted")
        return ride_planning.id

    def find_by_id_and_user_id(self, user_id: UserId, ride_planning_id: RidePlanningId) -> Optional[RidePlanningEntity]:
        self._logger.info(f"Find by user_id: {user_id} and ride_planning_id: {ride_planning_id}")
        item: Dict = self._dynamodb_resource_table.get_item(
            Key={
                str(PRIMARY_KEY): user_id,
                str(SORT_KEY): ride_planning_id
            },
            ConsistentRead=True
        )
        if "Item" in item:
            ride: Dict = item.get("Item")
            self._logger.info(f"Found item {ride}")
            return map_persistence_schema_to_ride_planning(ride)
