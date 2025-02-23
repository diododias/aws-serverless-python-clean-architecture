from datetime import datetime, UTC
import uuid
from unittest import mock

from request_ride_planning.application.notification_gateway_interface import NotificationGatewayInterface
from request_ride_planning.domain.entities.address_entity import AddressEntity
from request_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from request_ride_planning.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from request_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from request_ride_planning.domain.value_objects.user_id import UserId
from request_ride_planning.drivers_adapters.gateways.sns_notification_gateway import SnsNotificationGateway


class TestRidePlanningSnsGateway:
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
        id=RidePlanningId(mock_event.get("user_id")),
        user_id=UserId(mock_event.get("user_id")),
        address_from=AddressEntity(**mock_event.get("address_from")),
        address_to=AddressEntity(**mock_event.get("address_to")),
        status=RidePlanningStatusEnum.REQUESTED,
        departure_datetime=datetime.now(UTC),
        created_at=datetime.now(UTC),
        modified_at=datetime.now(UTC),
    )

    def test_return_ride_planning_id_when_execute_successfull(self):
        # arrange
        fake_message_id = "FAKE-MESSAGE-ID"
        sns_client_mock = mock.Mock()
        sns_client_mock.publish = mock.Mock(return_value={"MessageId": fake_message_id})
        sns_topic_arn = "FAKE-TOPIC-ARN"

        notification_gateway: NotificationGatewayInterface = (
            SnsNotificationGateway(sns_client_mock, sns_topic_arn))

        # act
        response = notification_gateway.notify_requested(self.ride_planning_mock)

        # assert
        assert response == fake_message_id
        sns_client_mock.publish.assert_called()
