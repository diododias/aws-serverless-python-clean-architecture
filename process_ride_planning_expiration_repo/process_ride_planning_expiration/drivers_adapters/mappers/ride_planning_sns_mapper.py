from process_ride_planning_expiration.domain.entities.ride_planning_entity import RidePlanningEntity
from process_ride_planning_expiration.domain.events.ride_planning_expired_event import RidePlanningExpiredEvent, \
    ExpirationPayload


def map_ride_planning_to_expired_event(
        ride_planning: RidePlanningEntity) -> RidePlanningExpiredEvent:
    return RidePlanningExpiredEvent(
        data=ExpirationPayload(
            ride_planning_id=ride_planning.id,
            user_id=ride_planning.user_id
        ),
        source="process_ride_planning_expiration"
    )
