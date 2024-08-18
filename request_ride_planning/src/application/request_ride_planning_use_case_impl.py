import datetime
import uuid
from aws_lambda_powertools import Logger

from src.application.too_many_requests_exception import TooManyRequestsException
from src.application.ride_planning_notification_gateway import RidePlanningNotificationGateway
from src.application.ride_planning_persistence_gateway import RidePlanningPersistenceGateway
from src.domain.entities.address_entity import AddressEntity
from src.domain.entities.ride_planning_entity import RidePlanningEntity
from src.domain.use_cases.request_ride_planning_use_case import RequestRidePlanningUseCase
from src.domain.value_objects.ride_planning_Id import RidePlanningId
from src.domain.value_objects.user_id import UserId


class RequestRidePlanningUseCaseImpl(RequestRidePlanningUseCase):
    _persistence_gateway: RidePlanningPersistenceGateway
    _notification_gateway: RidePlanningNotificationGateway
    _logger = Logger(child=True)

    def __init__(self,
                 persistence_gateway: RidePlanningPersistenceGateway,
                 notification_gateway: RidePlanningNotificationGateway):
        self._persistence_gateway = persistence_gateway
        self._notification_gateway = notification_gateway

    def _validate(self, user_id: UserId,
                        address_from: AddressEntity,
                        address_to: AddressEntity,
                        departure_datetime: datetime) -> None:
        rp: RidePlanningEntity = self._persistence_gateway.get_latest_by_user_id_ride_attributes(
            user_id,
            address_from,
            address_to,
            departure_datetime
        )
        if rp and not rp.is_done():
            raise TooManyRequestsException(rp)
        self._logger.info("Has no similar ride planning found")

    def execute(self,
                user_id: UserId,
                address_from: AddressEntity,
                address_to: AddressEntity,
                departure_datetime: datetime) -> RidePlanningId:
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
            departure_datetime=departure_datetime
        )
        self._persistence_gateway.save(ride_planning)
        self._logger.info(f"ride planning {ride_planning.id} was persisted")

        self._notification_gateway.send(ride_planning)
        self._logger.info(f"Ride planning {ride_planning.id} was created")
        return ride_planning.id
