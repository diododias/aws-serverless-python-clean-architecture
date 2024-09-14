import json
from typing import Optional

from aws_lambda_powertools import Logger

from process_ride_planning_expiration.application.ride_planning_not_found_exception import RidePlanningNotFoundException
from process_ride_planning_expiration.application.notification_gateway_interface import \
    NotificationGatewayInterface
from process_ride_planning_expiration.application.persistence_gateway_interface import \
    PersistenceGatewayInterface
from process_ride_planning_expiration.domain.entities.ride_planning_entity import RidePlanningEntity
from process_ride_planning_expiration.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from process_ride_planning_expiration.domain.use_cases.process_ride_planning_expiration_use_case_interface import \
    ProcessRidePlanningExpirationUseCaseInterface
from process_ride_planning_expiration.domain.value_objects.ride_planning_id import RidePlanningId
from process_ride_planning_expiration.domain.value_objects.user_id import UserId


class ProcessRidePlanningExpirationUseCaseImpl(ProcessRidePlanningExpirationUseCaseInterface):
    _persistence_gateway: PersistenceGatewayInterface
    _notification_gateway: NotificationGatewayInterface
    _logger = Logger(child=True)

    def __init__(self,
                 persistence_gateway: PersistenceGatewayInterface,
                 notification_gateway: NotificationGatewayInterface):
        self._persistence_gateway = persistence_gateway
        self._notification_gateway = notification_gateway

    def execute(self, user_id: UserId, ride_planning_id: RidePlanningId) -> RidePlanningEntity:
        ride_planning: RidePlanningEntity = self._persistence_gateway.find_by_id_and_user_id(user_id, ride_planning_id)
        if not ride_planning:
            raise RidePlanningNotFoundException(ride_planning_id)

        if ride_planning.status == RidePlanningStatusEnum.EXPIRED:
            self._logger.info(f"Ride planning {ride_planning.id} already expired")
            return ride_planning

        ride_planning.set_expiration_status()
        self._persistence_gateway.update(ride_planning)
        self._notification_gateway.notify_expired(ride_planning)
        return ride_planning
