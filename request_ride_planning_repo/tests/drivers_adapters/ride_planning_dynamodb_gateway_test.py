import copy
import json
from datetime import datetime, UTC
import uuid
from unittest import mock

from request_ride_planning.application.ride_planning_persistence_gateway_interface import RidePlanningPersistenceGatewayInterface
from request_ride_planning.domain.entities.address_entity import AddressEntity
from request_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from request_ride_planning.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from request_ride_planning.drivers_adapters.dynamodb_constants import PRIMARY_KEY, SORT_KEY
from request_ride_planning.drivers_adapters.gateways.ride_planning_dynamodb_gateway import RidePlanningDynamodbGateway


class TestRideDynamodbGateway:
    id = uuid.uuid4().hex
    user_payload = {
        "user_id": "cace4a159ff9f2512dd42373760608767b62855d",
        "status": RidePlanningStatusEnum.REQUESTED.value,
        "address_from": {
            "street": "Rua Augusta, 321",
            "city": "Sao Paulo",
            "country": "Brazil",
            "postal_code": "03881100",
        },
        "address_to": {
            "street": "Avenida 25 de Marco, 322",
            "city": "Sao Paulo",
            "country": "Brazil",
            "postal_code": "03881100",
        },
        "departure_datetime": "2024-12-01T05:33:20+00:00",
        "created_at": "2024-12-01T05:23:20+00:00",
        "modified_at": "2024-12-01T05:23:20+00:00"
    }
    ride_planning_mock = RidePlanningEntity(
        id=id,
        user_id=user_payload.get("user_id"),
        address_from=AddressEntity(**user_payload.get("address_from")),
        address_to=AddressEntity(**user_payload.get("address_to")),
        status=RidePlanningStatusEnum.REQUESTED,
        departure_datetime=datetime.now(UTC),
        created_at=datetime.now(UTC),
        modified_at=datetime.now(UTC)
    )

    def test_put_item_successfull_when_save_is_called(self):
        # arrange
        dynamodb_resource_table_mock = mock.Mock()
        dynamodb_resource_table_mock.put_item = mock.Mock()

        persistence_gateway: RidePlanningPersistenceGatewayInterface = (
            RidePlanningDynamodbGateway(dynamodb_resource_table_mock))

        # act
        ride_planning_id = persistence_gateway.save(self.ride_planning_mock)

        # assert
        assert ride_planning_id == self.ride_planning_mock.id
        dynamodb_resource_table_mock.put_item.assert_called()

    def test_return_none_when_has_no_latest(self):
        # arrange
        dynamodb_resource_table_mock = mock.Mock()
        dynamodb_resource_table_mock.query = mock.Mock(return_value=dict())

        persistence_gateway: RidePlanningPersistenceGatewayInterface = (
            RidePlanningDynamodbGateway(dynamodb_resource_table_mock))

        # act
        ride_planning_id = persistence_gateway.get_latest_by_user_id_ride_attributes(
            self.ride_planning_mock.user_id,
            self.ride_planning_mock.address_from,
            self.ride_planning_mock.address_to,
            self.ride_planning_mock.departure_datetime,
        )

        # assert
        assert ride_planning_id is None
        dynamodb_resource_table_mock.query.assert_called()

    def test_return_ride_planning_id_when_has_latest(self):
        # arrange
        query_mock = {
            "Items": [
                {
                    str(PRIMARY_KEY): self.user_payload.get(PRIMARY_KEY),
                    str(SORT_KEY): self.id
                }
            ]
        }
        event = copy.copy(self.user_payload)
        event["ride_planning_id"] = self.id
        event["address_from"] = json.dumps(self.user_payload.get("address_from"))
        event["address_to"] = json.dumps(self.user_payload.get("address_to"))
        event["created_at"] = self.user_payload.get("created_at")
        event["modified_at"] = self.user_payload.get("modified_at")
        item_mock = {
            "Item": event
        }
        dynamodb_resource_table_mock = mock.Mock()
        dynamodb_resource_table_mock.query = mock.Mock(return_value=query_mock)
        dynamodb_resource_table_mock.get_item = mock.Mock(return_value=item_mock)

        persistence_gateway: RidePlanningPersistenceGatewayInterface = (
            RidePlanningDynamodbGateway(dynamodb_resource_table_mock))

        # act
        ride_planning: RidePlanningEntity = persistence_gateway.get_latest_by_user_id_ride_attributes(
            self.ride_planning_mock.user_id,
            self.ride_planning_mock.address_from,
            self.ride_planning_mock.address_to,
            self.ride_planning_mock.departure_datetime
        )

        # assert
        assert ride_planning.id == self.id
        assert ride_planning.user_id == self.user_payload.get("user_id")
        assert ride_planning.status == self.user_payload.get("status")
        assert ride_planning.modified_at == datetime.fromisoformat(self.user_payload.get("modified_at"))
        assert ride_planning.created_at == datetime.fromisoformat(self.user_payload.get("created_at"))
        assert isinstance(ride_planning, RidePlanningEntity)
        dynamodb_resource_table_mock.query.assert_called()
