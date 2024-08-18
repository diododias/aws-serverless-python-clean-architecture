import datetime
import uuid
from unittest import mock

from src.domain.entities.address_entity import AddressEntity
from src.domain.entities.ride_planning_entity import RidePlanningEntity
from src.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from src.domain.value_objects.ride_planning_Id import RidePlanningId
from src.drivers_adapters.gateways.ride_planning_notification_gateway_impl import RidePlanningNotificationGatewayImpl


class TestRidePlanningNotificationGatewayImpl:
    mock_event = {
        "user_id": "cace4a159ff9f2512dd42373760608767b62855d",
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
        "departure_datetime": "2024-12-01T05:33:20.000Z"
    }
    id = uuid.uuid4().hex
    ride_planning_mock = RidePlanningEntity(
        id=id,
        user_id=mock_event.get("user_id"),
        address_from=AddressEntity(**mock_event.get("address_from")),
        address_to=AddressEntity(**mock_event.get("address_to")),
        status=RidePlanningStatusEnum.REQUESTED,
        departure_datetime=datetime.datetime.now()
    )

    def test_return_ride_planning_id_when_execute_successfull(self):
        # arrange
        fake_message_id = "FAKE-MESSAGE-ID"
        sns_client_mock = mock.Mock()
        sns_client_mock.publish = mock.Mock(return_value={"MessageId": fake_message_id})
        sns_topic_arn = "FAKE-TOPIC-ARN"

        notification_gateway = RidePlanningNotificationGatewayImpl(sns_client_mock, sns_topic_arn)

        # act
        response = notification_gateway.send(self.ride_planning_mock)

        # assert
        assert response == fake_message_id
        sns_client_mock.publish.assert_called()
