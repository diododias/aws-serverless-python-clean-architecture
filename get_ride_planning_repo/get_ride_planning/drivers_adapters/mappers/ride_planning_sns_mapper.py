from aws_lambda_powertools import Logger

from get_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from get_ride_planning.domain.events.ride_planning_waiting_for_expiration_event import \
    RidePlanningWaitingForExpirationEvent, ExpirationData

logger: Logger = Logger(child=True)


def map_ride_planning_to_waiting_for_expiration_event(
        ride_planning: RidePlanningEntity) -> RidePlanningWaitingForExpirationEvent:
    return RidePlanningWaitingForExpirationEvent(
        data=ExpirationData(
            ride_planning_id=ride_planning.id,
            user_id=ride_planning.user_id
        ),
        source="get_ride_planning",
        correlation_id=logger.get_correlation_id()
    )
