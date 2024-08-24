import uuid
from datetime import datetime, timedelta, UTC

from request_ride_planning.domain.entities.address_entity import AddressEntity
from request_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from request_ride_planning.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum


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

    def test_request_ride_planning_when_is_not_done(self):
        ride_planning = RidePlanningEntity(
            id=uuid.uuid4().hex,
            user_id=self.mock_event.get("user_id"),
            address_from=AddressEntity(**self.mock_event.get("address_from")),
            address_to=AddressEntity(**self.mock_event.get("address_to")),
            status=RidePlanningStatusEnum.REQUESTED,
            departure_datetime=datetime.now(UTC),
            created_at=datetime.now(UTC),
            modified_at=datetime.now(UTC)
        )
        assert not ride_planning.is_done()

    def test_request_ride_planning_when_time_expired_then_is_done(self):
        ride_planning = RidePlanningEntity(
            id=uuid.uuid4().hex,
            user_id=self.mock_event.get("user_id"),
            address_from=AddressEntity(**self.mock_event.get("address_from")),
            address_to=AddressEntity(**self.mock_event.get("address_to")),
            status=RidePlanningStatusEnum.REQUESTED,
            departure_datetime=datetime.now(UTC),
            created_at=datetime.now(UTC) - timedelta(minutes=10),
            modified_at=datetime.now(UTC)
        )
        assert ride_planning.is_done()

    def test_request_ride_planning_when_status_approved_then_is_done(self):
        ride_planning = RidePlanningEntity(
            id=uuid.uuid4().hex,
            user_id=self.mock_event.get("user_id"),
            address_from=AddressEntity(**self.mock_event.get("address_from")),
            address_to=AddressEntity(**self.mock_event.get("address_to")),
            status=RidePlanningStatusEnum.APPROVED,
            departure_datetime=datetime.now(UTC),
            created_at=datetime.now(UTC),
            modified_at=datetime.now(UTC)
        )
        assert ride_planning.is_done()

    def test_request_ride_planning_when_status_expired_then_is_done(self):
        ride_planning = RidePlanningEntity(
            id=uuid.uuid4().hex,
            user_id=self.mock_event.get("user_id"),
            address_from=AddressEntity(**self.mock_event.get("address_from")),
            address_to=AddressEntity(**self.mock_event.get("address_to")),
            status=RidePlanningStatusEnum.EXPIRED,
            departure_datetime=datetime.now(UTC),
            created_at=datetime.now(UTC),
            modified_at=datetime.now(UTC)
        )
        assert ride_planning.is_done()
