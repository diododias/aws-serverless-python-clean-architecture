

class RequestRideOptionFailException(Exception):
    def __init__(self):
        super().__init__(f"No partner returned the request")
