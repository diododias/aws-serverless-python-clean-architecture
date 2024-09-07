from process_ride_planning_expiration.infrastructure.config import start_app

process_ride_planning_expiration_handler = start_app()


def handler(event, context):
    return process_ride_planning_expiration_handler.handle(event, context)
