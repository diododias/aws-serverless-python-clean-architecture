from request_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity


class TooManyRequestsException(Exception):
    def __init__(self, ride_planning: RidePlanningEntity):
        super().__init__(f"Wait for a ride planning {ride_planning.id} to be completed before request a new ride "
                         f"planning")
