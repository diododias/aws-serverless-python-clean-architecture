from aws_lambda_powertools import Logger

from process_ride_planning_expiration.domain.entities.ride_planning_entity import RidePlanningEntity
from process_ride_planning_expiration.domain.events.ride_planning_expired_event import RidePlanningExpiredEvent, \
    ExpirationData

logger: Logger = Logger(child=True)


def map_ride_planning_to_expired_event(
        ride_planning: RidePlanningEntity) -> RidePlanningExpiredEvent:
    return RidePlanningExpiredEvent(
        data=ExpirationData(
            ride_planning_id=ride_planning.id,
            user_id=ride_planning.user_id
        ),
        source="process_ride_planning_expiration",
        correlation_id=logger.get_correlation_id()
    )
