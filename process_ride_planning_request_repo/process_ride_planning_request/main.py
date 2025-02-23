from process_ride_planning_request.infrastructure.config import start_app

process_ride_planning_request_handler = start_app()


def handler(event, context):
    return process_ride_planning_request_handler.handle(event, context)
