from get_ride_planning.application.ride_planning_not_found_exception import RidePlanningNotFound
from get_ride_planning.application.ride_planning_notification_gateway_interface import \
    RidePlanningNotificationGatewayInterface
from get_ride_planning.application.ride_planning_persistence_gateway_interface import \
    RidePlanningPersistenceGatewayInterface
from get_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from get_ride_planning.domain.use_cases.get_ride_planning_use_case_interface import GetRidePlanningUseCaseInterface
from get_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from get_ride_planning.domain.value_objects.user_id import UserId


class GetRidePlanningUseCaseImpl(GetRidePlanningUseCaseInterface):
    _persistence_gateway: RidePlanningPersistenceGatewayInterface
    _notification_gateway: RidePlanningNotificationGatewayInterface

    def __init__(self,
                 persistence_gateway: RidePlanningPersistenceGatewayInterface,
                 notification_gateway: RidePlanningNotificationGatewayInterface):
        self._persistence_gateway = persistence_gateway
        self._notification_gateway = notification_gateway

    def execute(self, user_id: UserId, ride_planning_id: RidePlanningId) -> RidePlanningEntity:
        ride_planning: RidePlanningEntity = self._persistence_gateway.find_by_id_and_user_id(
            user_id,
            ride_planning_id
        )
        if not ride_planning:
            raise RidePlanningNotFound(ride_planning_id)
        if ride_planning.check_waiting_for_expiration():
            self._notification_gateway.notify_waiting_for_expiration(ride_planning)
        return ride_planning
