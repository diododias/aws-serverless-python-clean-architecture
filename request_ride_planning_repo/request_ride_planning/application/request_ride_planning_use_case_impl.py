import dataclasses
import uuid

from datetime import datetime, UTC
from aws_lambda_powertools import Logger

from request_ride_planning.application.ride_planning_notification_gateway_interface import (
    RidePlanningNotificationGatewayInterface)
from request_ride_planning.application.ride_planning_persistence_gateway_interface import (
    RidePlanningPersistenceGatewayInterface)
from request_ride_planning.application.too_many_requests_error import TooManyRequestsError
from request_ride_planning.domain.entities.address_entity import AddressEntity
from request_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from request_ride_planning.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from request_ride_planning.domain.use_cases.request_ride_planning_use_case_interface import (
    RequestRidePlanningUseCaseInterface)
from request_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from request_ride_planning.domain.value_objects.user_id import UserId


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
        rp: RidePlanningEntity = self._persistence_gateway.find_latest_by_user_id_and_ride_attributes(
            user_id,
            address_from,
            address_to,
            departure_datetime
        )
        if rp is None:
            self._logger.info("Has no similar ride planning found in processing state")
            return
        if rp.check_waiting_for_expiration():
            self._notification_gateway.notify_waiting_for_expiration(rp)
            self._logger.info(f"Found Ride Planning id {rp.id} entering expiration state")
        if not rp.is_completed:
            raise TooManyRequestsError(rp)
        self._logger.info(f"User id {user_id} can request a new Ride Planning")

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
            id=RidePlanningId(uuid.uuid4().hex),
            user_id=user_id,
            address_from=address_from,
            address_to=address_to,
            departure_datetime=departure_datetime,
            status=RidePlanningStatusEnum.REQUESTED,
            created_at=datetime.now(UTC),
            modified_at=datetime.now(UTC)
        )
        self._persistence_gateway.save(ride_planning)
        self._logger.info(f"New ride planning {ride_planning.id} was persisted")

        self._notification_gateway.notify_requested(ride_planning)
        self._logger.info(f"Ride planning {ride_planning.id} request sent to be processed")
        return ride_planning.id
