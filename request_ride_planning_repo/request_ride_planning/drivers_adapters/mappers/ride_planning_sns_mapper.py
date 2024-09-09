from request_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from request_ride_planning.domain.events.ride_planning_requested_event import RidePlanningRequestedEvent, \
    RequestedPayload
from request_ride_planning.domain.events.ride_planning_waiting_for_expiration_event import ExpirationPayload, \
    RidePlanningWaitingForExpirationEvent


def map_ride_planning_to_waiting_for_expiration_event(
        ride_planning: RidePlanningEntity) -> RidePlanningWaitingForExpirationEvent:
    return RidePlanningWaitingForExpirationEvent(
        data=ExpirationPayload(
            ride_planning_id=ride_planning.id,
            user_id=ride_planning.user_id
        ),
        source="request_ride_planning"
    )


def map_ride_planning_to_requested_event(
        ride_planning: RidePlanningEntity) -> RidePlanningRequestedEvent:
    return RidePlanningRequestedEvent(
        data=RequestedPayload(
            ride_planning_id=ride_planning.id,
            user_id=ride_planning.user_id
        ),
        source="request_ride_planning"
    )
