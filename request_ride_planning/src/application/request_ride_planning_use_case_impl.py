import uuid

from datetime import datetime, UTC
from aws_lambda_powertools import Logger

from src.application.too_many_requests_exception import TooManyRequestsException
from src.application.ride_planning_notification_gateway_interface import RidePlanningNotificationGatewayInterface
from src.application.ride_planning_persistence_gateway_interface import RidePlanningPersistenceGatewayInterface
from src.domain.entities.address_entity import AddressEntity
from src.domain.entities.ride_planning_entity import RidePlanningEntity
from src.domain.use_cases.request_ride_planning_use_case_interface import RequestRidePlanningUseCaseInterface
from src.domain.value_objects.ride_planning_id import RidePlanningId
from src.domain.value_objects.user_id import UserId

TZ = "America/Sao_Paulo"


class RequestRidePlanningUseCaseImpl(RequestRidePlanningUseCaseInterface):
    _persistence_gateway: RidePlanningPersistenceGatewayInterface
    _notification_gateway: RidePlanningNotificationGatewayInterface
    _logger = Logger(child=True)

    def __init__(self,
                 persistence_gateway: RidePlanningPersistenceGatewayInterface,
                 notification_gateway: RidePlanningNotificationGatewayInterface):
        self._persistence_gateway = persistence_gateway
        self._notification_gateway = notification_gateway

    def _validate(self, user_id: UserId,
                  address_from: AddressEntity,
                  address_to: AddressEntity,
                  departure_datetime: datetime) -> None:
        """
        Checks if exists a ride planning with the same attributes in the processing stage.
        Only one ride can be requested at a time.

        Args:
            user_id: User ID
            address_from: start point of a ride
            address_to: end point of a ride
            departure_datetime: date and time to start a ride

        Returns: None

        Raises:
            TooManyRequestsException
        """
        rp: RidePlanningEntity = self._persistence_gateway.get_latest_by_user_id_ride_attributes(
            user_id,
            address_from,
            address_to,
            departure_datetime
        )
        if rp and not rp.is_done():
            raise TooManyRequestsException(rp)
        self._logger.info("Has no similar ride planning found in processing state")

    def execute(self,
                user_id: UserId,
                address_from: AddressEntity,
                address_to: AddressEntity,
                departure_datetime: datetime) -> RidePlanningId:
        """
        Request a new Ride Planning to be processed

        Args:
            user_id: User ID
            address_from: start point of a ride
            address_to: end point of a ride
            departure_datetime: date and time to start a ride

        Returns: RidePlanningId of a new ride planning request
        """
        self._validate(
            user_id,
            address_from,
            address_to,
            departure_datetime
        )
        ride_planning: RidePlanningEntity = RidePlanningEntity(
            id=uuid.uuid4().hex,
            user_id=user_id,
            address_from=address_from,
            address_to=address_to,
            departure_datetime=departure_datetime,
            created_at=datetime.now(UTC),
            modified_at=datetime.now(UTC)
        )
        self._persistence_gateway.save(ride_planning)
        self._logger.info(f"ride planning {ride_planning.id} was persisted")

        self._notification_gateway.send(ride_planning)
        self._logger.info(f"Ride planning {ride_planning.id} was created")
        return ride_planning.id
