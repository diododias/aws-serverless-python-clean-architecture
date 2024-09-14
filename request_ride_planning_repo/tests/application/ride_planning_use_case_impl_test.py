import copy
import uuid
from datetime import datetime, UTC
from unittest import mock

import pytest

from request_ride_planning.application.request_ride_planning_use_case_impl import RequestRidePlanningUseCaseImpl
from request_ride_planning.application.notification_gateway_interface import \
    NotificationGatewayInterface
from request_ride_planning.application.persistence_gateway_interface import \
    PersistenceGatewayInterface
from request_ride_planning.application.too_many_requests_exception import TooManyRequestsException
from request_ride_planning.domain.entities.address_entity import AddressEntity
from request_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from request_ride_planning.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from request_ride_planning.domain.use_cases.request_ride_planning_use_case_interface import \
    RequestRidePlanningUseCaseInterface
from request_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from request_ride_planning.domain.value_objects.user_id import UserId


class TestRidePlanningUseCaseImpl:
    mock_event = {
        "id": "d39d5e8ed9c04096a65f679468600db1",
        "user_id": "cace4a159ff9f2512dd42373760608767b62855d",
        "address_from": {
            "street": "Rua Augusta, 321",
            "city": "Sao Paulo",
            "country": "Brazil",
            "postal_code": "03881100"
        },
        "address_to": {
            "street": "Rua Augusta, 321",
            "city": "Sao Paulo",
            "country": "Brazil",
            "postal_code": "03881100"
        },
        "departure_datetime": "2024-12-01 05:33:20+00:00",
        "created_at": "2024-08-30 01:38:09+00:00",
        "modified_at": "2024-08-30 01:38:09+00:00",
        "status": "REQUESTED",
        "ride_options": []
    }
    ride_planning_mock = RidePlanningEntity(
        id=RidePlanningId(mock_event.get("id")),
        user_id=UserId(mock_event.get("user_id")),
        address_from=AddressEntity(**mock_event.get("address_from")),
        address_to=AddressEntity(**mock_event.get("address_to")),
        status=RidePlanningStatusEnum.REQUESTED,
        departure_datetime=datetime.now(UTC),
        created_at=datetime.now(UTC),
        modified_at=datetime.now(UTC)
    )

    def test_return_ride_planning_id_when_execute_successfull(self):
        # arrange
        notification_gateway_mock = mock.Mock(spec=NotificationGatewayInterface)
        notification_gateway_mock.send = mock.Mock()

        persistence_gateway_mock = mock.Mock(spec=PersistenceGatewayInterface)
        persistence_gateway_mock.save = mock.Mock()
        # has no one ride planning in execution state
        persistence_gateway_mock.get_latest_by_user_id_ride_attributes = mock.Mock(return_value=None)

        use_case: RequestRidePlanningUseCaseInterface = (
            RequestRidePlanningUseCaseImpl(persistence_gateway_mock, notification_gateway_mock))

        # act
        ride_planning_id: RidePlanningId = use_case.execute(
            user_id=UserId(self.mock_event.get("user_id")),
            address_from=AddressEntity(**self.mock_event.get("address_from")),
            address_to=AddressEntity(**self.mock_event.get("address_to")),
            departure_datetime=datetime.fromisoformat(self.mock_event.get("departure_datetime"))
        )

        # assert
        assert isinstance(ride_planning_id, RidePlanningId)
        persistence_gateway_mock.save.assert_called()
        persistence_gateway_mock.find_latest_by_user_id_and_ride_attributes.assert_called()
        notification_gateway_mock.notify_requested.assert_called()

    def test_explode_too_many_requests_exception_when_has_ride_planning_executing(self):
        # arrange
        notification_gateway_mock = mock.Mock(spec=NotificationGatewayInterface)
        notification_gateway_mock.send = mock.Mock()

        persistence_gateway_mock = mock.Mock(spec=PersistenceGatewayInterface)
        persistence_gateway_mock.save = mock.Mock()
        # return ride planning in execution state
        persistence_gateway_mock.find_latest_by_user_id_and_ride_attributes = mock.Mock(return_value=self.ride_planning_mock)

        use_case: RequestRidePlanningUseCaseInterface = (
            RequestRidePlanningUseCaseImpl(persistence_gateway_mock, notification_gateway_mock))

        # act
        with pytest.raises(TooManyRequestsException):
            use_case.execute(
                user_id=UserId(self.mock_event.get("user_id")),
                address_from=AddressEntity(**self.mock_event.get("address_from")),
                address_to=AddressEntity(**self.mock_event.get("address_to")),
                departure_datetime=datetime.fromisoformat(self.mock_event.get("departure_datetime"))
            )

        # assert
        persistence_gateway_mock.save.assert_not_called()
        persistence_gateway_mock.find_latest_by_user_id_and_ride_attributes.assert_called()
        notification_gateway_mock.notify_requested.assert_not_called()

    def test_return_ride_planning_id_when_latest_ride_planning_is_done(self):
        # arrange
        notification_gateway_mock = mock.Mock(spec=NotificationGatewayInterface)
        notification_gateway_mock.send = mock.Mock()

        persistence_gateway_mock = mock.Mock(spec=PersistenceGatewayInterface)
        persistence_gateway_mock.save = mock.Mock()
        # ride planning in execution done state
        rp_mock = copy.copy(self.ride_planning_mock)
        rp_mock.status = RidePlanningStatusEnum.APPROVED
        persistence_gateway_mock.get_latest_by_user_id_ride_attributes = mock.Mock(return_value=rp_mock)

        use_case: RequestRidePlanningUseCaseInterface = (
            RequestRidePlanningUseCaseImpl(persistence_gateway_mock, notification_gateway_mock))

        # act
        ride_planning_id: RidePlanningId = use_case.execute(
            user_id=UserId(self.mock_event.get("user_id")),
            address_from=AddressEntity(**self.mock_event.get("address_from")),
            address_to=AddressEntity(**self.mock_event.get("address_to")),
            departure_datetime=datetime.fromisoformat(self.mock_event.get("departure_datetime"))
        )

        # assert
        assert isinstance(ride_planning_id, RidePlanningId)
        persistence_gateway_mock.save.assert_called()
        persistence_gateway_mock.find_latest_by_user_id_and_ride_attributes.assert_called()
        notification_gateway_mock.notify_requested.assert_called()
