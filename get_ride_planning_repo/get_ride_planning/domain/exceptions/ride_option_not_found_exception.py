from process_ride_planning_expiration.domain.value_objects.ride_option_id import RideOptionId


class RideOptionNotFoundException(Exception):
    def __init__(self, ride_option_id: RideOptionId):
        super().__init__(f"Ride Option id {ride_option_id} not found")
