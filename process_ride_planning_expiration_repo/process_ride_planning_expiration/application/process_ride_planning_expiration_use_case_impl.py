from aws_lambda_powertools import Logger

from process_ride_planning_expiration.application.ride_planning_not_found_exception import RidePlanningNotFound
from process_ride_planning_expiration.application.ride_planning_notification_gateway_interface import \
    RidePlanningNotificationGatewayInterface
from process_ride_planning_expiration.application.ride_planning_persistence_gateway_interface import \
    RidePlanningPersistenceGatewayInterface
from process_ride_planning_expiration.domain.entities.ride_planning_entity import RidePlanningEntity
from process_ride_planning_expiration.domain.entities.ride_planning_status_enum import RidePlanningStatusEnum
from process_ride_planning_expiration.domain.use_cases.process_ride_planning_expiration_use_case_interface import \
    ProcessRidePlanningExpirationUseCaseInterface
from process_ride_planning_expiration.domain.value_objects.ride_planning_id import RidePlanningId
from process_ride_planning_expiration.domain.value_objects.user_id import UserId


class ProcessRidePlanningExpirationUseCaseImpl(ProcessRidePlanningExpirationUseCaseInterface):
    _persistence_gateway: RidePlanningPersistenceGatewayInterface
    _notification_gateway: RidePlanningNotificationGatewayInterface
    _logger = Logger(child=True)

    def __init__(self,
                 persistence_gateway: RidePlanningPersistenceGatewayInterface,
                 notification_gateway: RidePlanningNotificationGatewayInterface):
        self._persistence_gateway = persistence_gateway
        self._notification_gateway = notification_gateway

    def execute(self, user_id: UserId, ride_planning_id: RidePlanningId) -> RidePlanningEntity:
        ride_planning: RidePlanningEntity = self._persistence_gateway.find_by_id_and_user_id(user_id, ride_planning_id)
        if not ride_planning:
            raise RidePlanningNotFound(ride_planning_id)
        if ride_planning.status == RidePlanningStatusEnum.EXPIRED:
            return ride_planning
        ride_planning.set_expiration_status()
        self._persistence_gateway.update(ride_planning)
        self._notification_gateway.notify_expired(ride_planning)
        self._logger.info(f"Ride planning {ride_planning.id} was expired")
        return ride_planning
