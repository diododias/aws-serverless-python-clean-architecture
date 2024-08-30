import uuid
from datetime import datetime, timedelta, UTC

import pytest

from get_ride_planning.domain.entities.address_entity import AddressEntity
from get_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from get_ride_planning.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from get_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from get_ride_planning.domain.value_objects.user_id import UserId


class TestRequestRidePlanningEntity:
    mock_event = {
        "user_id": "cace4a159ff9f2512dd42373760608767b62855d",
        "address_from": {
            "street": "Rua Augusta, 321",
            "city": "Sao Paulo",
            "country": "Brazil",
            "postal_code": "03881100"
        },
        "address_to": {
            "street": "Avenida 25 de Marco, 322",
            "city": "Sao Paulo",
            "country": "Brazil",
            "postal_code": "03881100"
        },
        "departure_datetime": "2024-12-01T05:33:20.000Z"
    }

    @pytest.mark.parametrize("not_completed_status", [RidePlanningStatusEnum.WAITING_FOR_EXPIRATION,
                                                      RidePlanningStatusEnum.WAITING_FOR_APPROVAL,
                                                      RidePlanningStatusEnum.REQUESTED])
    def test_given_ride_planning_when_status_is_not_in_completed_stage(self, not_completed_status):
        ride_planning = RidePlanningEntity(
            id=RidePlanningId(uuid.uuid4().hex),
            user_id=UserId(self.mock_event.get("user_id")),
            address_from=AddressEntity(**self.mock_event.get("address_from")),
            address_to=AddressEntity(**self.mock_event.get("address_to")),
            status=not_completed_status,
            departure_datetime=datetime.now(UTC),
            created_at=datetime.now(UTC),
            modified_at=datetime.now(UTC)
        )
        assert not ride_planning.is_completed

    def test_given_ride_planning_when_time_expired_then_is_completed(self):
        ride_planning = RidePlanningEntity(
            id=RidePlanningId(uuid.uuid4().hex),
            user_id=UserId(self.mock_event.get("user_id")),
            address_from=AddressEntity(**self.mock_event.get("address_from")),
            address_to=AddressEntity(**self.mock_event.get("address_to")),
            status=RidePlanningStatusEnum.REQUESTED,
            departure_datetime=datetime.now(UTC),
            created_at=datetime.now(UTC) - timedelta(minutes=10),
            modified_at=datetime.now(UTC)
        )
        assert ride_planning.is_completed

    @pytest.mark.parametrize("completed_status", [RidePlanningStatusEnum.APPROVED,
                                                  RidePlanningStatusEnum.EXPIRED,
                                                  RidePlanningStatusEnum.REQUEST_FAILED])
    def test_given_ride_planning_when_status_is_in_completed_stage(self, completed_status):
        ride_planning = RidePlanningEntity(
            id=RidePlanningId(uuid.uuid4().hex),
            user_id=UserId(self.mock_event.get("user_id")),
            address_from=AddressEntity(**self.mock_event.get("address_from")),
            address_to=AddressEntity(**self.mock_event.get("address_to")),
            status=completed_status,
            departure_datetime=datetime.now(UTC),
            created_at=datetime.now(UTC),
            modified_at=datetime.now(UTC)
        )
        assert ride_planning.is_completed

    @pytest.mark.parametrize("expired_status", [RidePlanningStatusEnum.REQUESTED,
                                                RidePlanningStatusEnum.WAITING_FOR_APPROVAL])
    def test_given_ride_planning_when_status_is_in_is_pending_expired_status_update(self, expired_status):
        ride_planning = RidePlanningEntity(
            id=RidePlanningId(uuid.uuid4().hex),
            user_id=UserId(self.mock_event.get("user_id")),
            address_from=AddressEntity(**self.mock_event.get("address_from")),
            address_to=AddressEntity(**self.mock_event.get("address_to")),
            status=expired_status,
            departure_datetime=datetime.now(UTC),
            created_at=datetime.now(UTC) - timedelta(minutes=10),
            modified_at=datetime.now(UTC)
        )
        assert ride_planning.check_waiting_for_expiration()

    def test_given_ride_planning_when_set_status_to_expired(self):
        ride_planning = RidePlanningEntity(
            id=RidePlanningId(uuid.uuid4().hex),
            user_id=UserId(self.mock_event.get("user_id")),
            address_from=AddressEntity(**self.mock_event.get("address_from")),
            address_to=AddressEntity(**self.mock_event.get("address_to")),
            status=RidePlanningStatusEnum.REQUESTED,
            departure_datetime=datetime.now(UTC),
            created_at=datetime.now(UTC) - timedelta(minutes=10),
            modified_at=datetime.now(UTC)
        )
        ride_planning.set_status_to_expired()
        assert ride_planning.status == RidePlanningStatusEnum.EXPIRED
