from get_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId


class RidePlanningNotFound(Exception):
    def __init__(self, ride_planning_id: RidePlanningId):
        super().__init__(f"Ride Planning id {ride_planning_id} not found")
