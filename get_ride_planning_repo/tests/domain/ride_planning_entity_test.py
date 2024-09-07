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

    @pytest.mark.parametrize("processing_status", [RidePlanningStatusEnum.REQUESTED,
                                                   RidePlanningStatusEnum.WAITING_FOR_APPROVAL])
    def test_given_ride_planning_when_check_waiting_expiration(self, processing_status):
        ride_planning = RidePlanningEntity(
            id=RidePlanningId(uuid.uuid4().hex),
            user_id=UserId(self.mock_event.get("user_id")),
            address_from=AddressEntity(**self.mock_event.get("address_from")),
            address_to=AddressEntity(**self.mock_event.get("address_to")),
            status=processing_status,
            departure_datetime=datetime.now(UTC),
            created_at=datetime.now(UTC) - timedelta(minutes=10),
            modified_at=datetime.now(UTC)
        )
        assert ride_planning.check_waiting_for_expiration()
        assert ride_planning.status == RidePlanningStatusEnum.WAITING_FOR_EXPIRATION
