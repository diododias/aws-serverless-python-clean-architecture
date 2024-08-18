from src.infrastructure.config import start_app

request_ride_planning_handler = start_app()


def handler(event, context):
    return request_ride_planning_handler.handle(event, context)
