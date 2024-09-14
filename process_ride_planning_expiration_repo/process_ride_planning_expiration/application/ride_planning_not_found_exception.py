from process_ride_planning_expiration.domain.value_objects.ride_planning_id import RidePlanningId


class RidePlanningNotFoundException(Exception):
    def __init__(self, ride_planning_id: RidePlanningId):
        super().__init__(f"Ride Planning id {ride_planning_id} not found")
