from process_ride_planning_request.application.gateways.notification_gateway_interface import NotificationGatewayInterface
from process_ride_planning_request.application.gateways.persistence_gateway_interface import PersistenceGatewayInterface
from process_ride_planning_request.application.exceptions.ride_planning_not_found_exception import RidePlanningNotFoundException
from process_ride_planning_request.domain.entities.ride_planning_entity import RidePlanningEntity
from process_ride_planning_request.application.exceptions.request_ride_option_fail_exception import \
    RequestRideOptionFailException
from process_ride_planning_request.domain.use_cases.process_ride_planning_request_use_case_interface import \
    ProcessRidePlanningRequestUseCaseInterface
from process_ride_planning_request.domain.use_cases.request_ride_options_from_partners_use_case_interface import \
    RequestRideOptionsFromPartnersUseCaseInterface
from process_ride_planning_request.domain.value_objects.ride_planning_id import RidePlanningId
from process_ride_planning_request.domain.value_objects.user_id import UserId


class ProcessRidePlanningRequestUseCaseImpl(ProcessRidePlanningRequestUseCaseInterface):
    _persistence_gateway: PersistenceGatewayInterface
    _notification_gateway: NotificationGatewayInterface
    _request_ride_options_use_case: RequestRideOptionsFromPartnersUseCaseInterface

    def __init__(self,
                 _persistence_gateway: PersistenceGatewayInterface,
                 _notification_gateway: NotificationGatewayInterface,
                 _request_ride_options_use_case: RequestRideOptionsFromPartnersUseCaseInterface
    ):
        self._persistence_gateway = _persistence_gateway
        self._notification_gateway = _notification_gateway
        self._request_ride_options_use_case = _request_ride_options_use_case

    def execute(self, user_id: UserId, ride_planning_id: RidePlanningId) -> RidePlanningEntity:
        ride_planning: RidePlanningEntity = self._persistence_gateway.find_by_id_and_user_id(
            user_id,
            ride_planning_id
        )
        if not ride_planning:
            raise RidePlanningNotFoundException(ride_planning_id)

        self._request_ride_options_use_case.execute(ride_planning)

        if not ride_planning.ride_options:
            raise RequestRideOptionFailException()

        ride_planning.set_waiting_for_approval_status()
        self._persistence_gateway.update(ride_planning)
        self._notification_gateway.notify_waiting_for_approve(ride_planning)
        return ride_planning
